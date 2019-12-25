import json
from decouple import config
from requests import Session

from grpc_adenine import settings
from grpc_adenine.settings import REQUEST_TIMEOUT
from grpc_adenine.stubs import hive_pb2
from grpc_adenine.stubs import hive_pb2_grpc
from grpc_adenine.implementations.utils import validate_api_key, get_encrypt_key, check_rate_limit
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
        self.session = Session()
        self.headers = {
            "general": headers_general,
            "hive": headers_hive
        }
        self.rate_limiter = RateLimiter()

    def UploadAndSign(self, request, context):

        api_key = request.api_key
        # Validate the API Key
        api_status = validate_api_key(api_key)
        if not api_status:
            response = {
                'result': {
                    'API_Key': api_key
                }
            }
            return hive_pb2.Response(output=json.dumps(response), status_message='API Key could not be verified', status=False)

        # Check whether the user is able to use this API by checking their rate limiter
        response = check_rate_limit(self.rate_limiter, settings.UPLOAD_AND_SIGN_LIMIT, api_key, self.UploadAndSign.__name__)
        if response:
            return hive_pb2.Response(output=json.dumps(response),
                                     status_message='Number of daily access limit exceeded',
                                     status=False)

        # reading the file content
        request_input = json.loads(request.input)

        # encoding and encrypting
        key = get_encrypt_key(request_input['private_key'])
        file_contents = request_input['file'].encode()
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(file_contents)

        # upload file to hive
        api_url_base = config('PRIVATE_NET_IP_ADDRESS') + config('HIVE_PORT') + settings.HIVE_API_ADD_FILE
        response = self.session.get(api_url_base, files={'file': encrypted_message}, headers=self.headers['hive'],
                                    timeout=REQUEST_TIMEOUT)
        data = json.loads(response.text)
        file_hash = data['Hash']

        if not data:
            status_message = 'Error: File could not be uploaded'
            status = False
            return hive_pb2.Response(output="", status_message=status_message, status=status)

        # signing the hash key
        private_key = request_input['private_key']
        did_api_url = config('PRIVATE_NET_IP_ADDRESS') + config('DID_SERVICE_URL') + settings.DID_SERVICE_API_SIGN
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
        response = {
            'result': data['result']
        }

        return hive_pb2.Response(output=json.dumps(response), status_message=status_message, status=status)

    def VerifyAndShow(self, request, context):

        api_key = request.api_key
        # Validate the API Key
        api_status = validate_api_key(api_key)
        if not api_status:
            response = {
                'result': {
                    'API_Key': api_key
                }
            }
            return hive_pb2.Response(output=json.dumps(response), status_message='API Key could not be verified', status=False)

        # Check whether the user is able to use this API by checking their rate limiter
        response = check_rate_limit(self.rate_limiter, settings.VERIFY_AND_SHOW_LIMIT, api_key, self.VerifyAndShow.__name__)
        if response:
            return hive_pb2.Response(output=json.dumps(response),
                                     status_message='Number of daily access limit exceeded',
                                     status=False)

        # verify the hash key
        request_input = json.loads(request.input)

        signed_message = request_input['msg']
        json_data = {
            "msg": signed_message,
            "pub": request_input['pub'],
            "sig": request_input['sig']
        }
        api_url_base = config('PRIVATE_NET_IP_ADDRESS') + config('DID_SERVICE_URL') + settings.DID_SERVICE_API_VERIFY
        response = self.session.post(api_url_base, data=json.dumps(json_data), headers=self.headers['general'],
                                     timeout=REQUEST_TIMEOUT)
        data = json.loads(response.text)
        if not data['result']:
            return hive_pb2.Response(output="", status_message='Hash key could not be verified', status=False)

        # verify the given input message using private key
        api_url_base = config('PRIVATE_NET_IP_ADDRESS') + config('DID_SERVICE_URL') + settings.DID_SERVICE_API_SIGN
        req_data = {
            "privateKey": request_input['private_key'],
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
        api_url_base = config('PRIVATE_NET_IP_ADDRESS') + config('HIVE_PORT') + settings.HIVE_API_RETRIEVE_FILE + "{}"
        response = self.session.get(api_url_base.format(request_input['hash']), timeout=REQUEST_TIMEOUT)

        # decrypt message
        key = get_encrypt_key(request_input['private_key'])
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(response.text.encode())

        response = {
            'result': {
                'output': decrypted_message.decode()
            }
        }

        return hive_pb2.Response(output=json.dumps(response), status_message='Successfully retrieved file from Elastos Hive', status=True)
