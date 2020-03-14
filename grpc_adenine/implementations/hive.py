import json
from decouple import config
from requests import Session
import logging
import sys
import jwt
import datetime
from sqlalchemy.orm import sessionmaker

from grpc_adenine import settings
from grpc_adenine.database import db_engine
from grpc_adenine.settings import REQUEST_TIMEOUT
from grpc_adenine.stubs.python import hive_pb2, hive_pb2_grpc
from grpc_adenine.implementations.utils import validate_api_key, get_encrypt_key, get_did_from_api, get_api_from_did
from grpc_adenine.implementations.rate_limiter import RateLimiter
from cryptography.fernet import Fernet


class Hive(hive_pb2_grpc.HiveServicer):

    def __init__(self):
        headers_general = {
            'Accepts': 'application/json',
            'Content-Type': 'application/json'
        }
        headers_hive = {'Content-Disposition': 'multipart/form-data;boundary'
                                               '=--------------------------608819652137318562927303'}
        self.headers = {
            "general": headers_general,
            "hive": headers_hive
        }
        self.session = Session()
        session_maker = sessionmaker(bind=db_engine)
        self.rate_limiter = RateLimiter(session_maker())
        self.TOKEN_EXPIRATION = 24 * 30

    def UploadAndSign(self, request, context):

        metadata = dict(context.invocation_metadata())
        did = metadata["did"]
        api_key = get_api_from_did(did)

        try:
            jwt_info = jwt.decode(request.input, key=api_key, algorithms=['HS256']).get('jwt_info')
        except:
            return hive_pb2.Response(output='', status_message='Authentication Error', status=False)

        network = jwt_info['network']

        # Validate the API Key
        api_status = validate_api_key(api_key)
        if not api_status:
            response = {
                'result': {
                    'API_Key': api_key
                }
            }
            status_message = "API Key could not be verified"
            logging.debug(f"{did} : {api_key} : {status_message}")
            return hive_pb2.Response(output=json.dumps(response), status_message=status_message, status=False)

        # Check whether the user is able to use this API by checking their rate limiter
        response = self.rate_limiter.check_rate_limit(settings.UPLOAD_AND_SIGN_LIMIT, api_key,
                                    self.UploadAndSign.__name__)
        if response:
            return hive_pb2.Response(output=json.dumps(response),
                                     status_message=f'Number of daily access limit exceeded {response["result"]["daily_limit"]}',
                                     status=False)

        # reading the file content
        encrypted_message = jwt_info['file_content'].encode("utf-8")

        # reading input data
        private_key = jwt_info['privateKey']

        # checking file size
        if sys.getsizeof(encrypted_message) > settings.FILE_UPLOAD_SIZE_LIMIT:
            return hive_pb2.Response(output="", status_message="File size limit exceeded", status=False)

        # upload file to hive
        api_url_base = config('PRIVATE_NET_HIVE_PORT') + settings.HIVE_API_ADD_FILE
        response = self.session.get(api_url_base, files={'file': encrypted_message}, headers=self.headers['hive'],
                                    timeout=REQUEST_TIMEOUT)
        data = json.loads(response.text)
        file_hash = data['Hash']

        if not data:
            status_message = 'Error: File could not be uploaded'
            status = False
            return hive_pb2.Response(output="", status_message=status_message, status=status)

        # signing the hash key
        if network == "testnet":
            did_api_url = config('TEST_NET_DID_SERVICE_URL') + settings.DID_SERVICE_API_SIGN
        else:
            did_api_url = config('PRIVATE_NET_DID_SERVICE_URL') + settings.DID_SERVICE_API_SIGN
        req_data = {
            "privateKey": private_key,
            "msg": file_hash
        }
        response = self.session.post(did_api_url, data=json.dumps(req_data), headers=self.headers['general'],
                                     timeout=REQUEST_TIMEOUT)
        data = json.loads(response.text)
        data['result']['hash'] = file_hash

        if data['status'] == 200:
            status_message = 'Successfully uploaded file to Elastos Hive'
            status = True
        else:
            status_message = 'Error'
            status = False

        del data['status']

        #generate jwt token
        jwt_info = {
            'result': data['result']
        }

        jwt_token = jwt.encode({
            'jwt_info': jwt_info,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=self.TOKEN_EXPIRATION)
        }, api_key, algorithm='HS256')

        return hive_pb2.Response(output=jwt_token, status_message=status_message, status=status)

    def VerifyAndShow(self, request, context):

        metadata = dict(context.invocation_metadata())
        did = metadata["did"]
        api_key = get_api_from_did(did)

        try:
            jwt_info = jwt.decode(request.input, key=api_key, algorithms=['HS256']).get('jwt_info')
        except:
            return hive_pb2.Response(output='', status_message='Authentication Error', status=False)

        network = jwt_info['network']

        # Validate the API Key
        api_status = validate_api_key(api_key)
        if not api_status:
            response = {
                'result': {
                    'API_Key': api_key
                }
            }
            return hive_pb2.Response(output=json.dumps(response), status_message='API Key could not be verified',
                                     status=False)

        # Check whether the user is able to use this API by checking their rate limiter
        response = self.rate_limiter.check_rate_limit(settings.VERIFY_AND_SHOW_LIMIT, api_key,
                                    self.VerifyAndShow.__name__)
        if response:
            return hive_pb2.Response(output=json.dumps(response),
                                     status_message=f'Number of daily access limit exceeded {response["result"]["daily_limit"]}',
                                     status=False)

        # verify the hash key
        request_input = jwt_info['request_input']

        signed_message = request_input['msg']
        json_data = {
            "msg": signed_message,
            "pub": request_input['pub'],
            "sig": request_input['sig']
        }
        if network == "testnet":
            api_url_base = config('TEST_NET_DID_SERVICE_URL') + settings.DID_SERVICE_API_VERIFY
        else:
            api_url_base = config('PRIVATE_NET_DID_SERVICE_URL') + settings.DID_SERVICE_API_VERIFY
        response = self.session.post(api_url_base, data=json.dumps(json_data), headers=self.headers['general'],
                                     timeout=REQUEST_TIMEOUT)
        data = json.loads(response.text)
        if not data['result']:
            return hive_pb2.Response(output="", status_message='Hash key could not be verified', status=False)

        # verify the given input message using private key
        if network == "testnet":
            api_url_base = config('TEST_NET_DID_SERVICE_URL') + settings.DID_SERVICE_API_SIGN
        else:
            api_url_base = config('PRIVATE_NET_DID_SERVICE_URL') + settings.DID_SERVICE_API_SIGN
        req_data = {
            "privateKey": request_input['privateKey'],
            "msg": request_input['hash']
        }
        response = self.session.post(api_url_base, data=json.dumps(req_data), headers=self.headers['general'],
                                     timeout=REQUEST_TIMEOUT)
        data = json.loads(response.text)
        if data['status'] != 200:
            return hive_pb2.Response(output="", status_message='Hash Key and message could not be verified',
                                     status=False)

        if data['result']['msg'] != signed_message:
            return hive_pb2.Response(output="", status_message='Hash Key and message could not be verified',
                                     status=False)

        # show content
        api_url_base = config('PRIVATE_NET_HIVE_PORT') + settings.HIVE_API_RETRIEVE_FILE + "{}"
        response = self.session.get(api_url_base.format(request_input['hash']), timeout=REQUEST_TIMEOUT)

        #generate jwt token
        jwt_info = {
            'file_content': response.text
        }

        jwt_token = jwt.encode({
            'jwt_info': jwt_info,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=self.TOKEN_EXPIRATION)
        }, api_key, algorithm='HS256')

        return hive_pb2.Response(output=jwt_token, status_message='Successfully retrieved file from Elastos Hive', status=True)
