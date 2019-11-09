# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common.proto',
  package='common',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0c\x63ommon.proto\x12\x06\x63ommon\"-\n\nApiRequest\x12\x12\n\nsecret_key\x18\x01 \x01(\t\x12\x0b\n\x03\x64id\x18\x02 \x01(\t\"F\n\x0b\x41piResponse\x12\x0f\n\x07\x61pi_key\x18\x01 \x01(\t\x12\x16\n\x0estatus_message\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\x05\x32I\n\x06\x43ommon\x12?\n\x12GenerateAPIRequest\x12\x12.common.ApiRequest\x1a\x13.common.ApiResponse\"\x00\x62\x06proto3')
)




_APIREQUEST = _descriptor.Descriptor(
  name='ApiRequest',
  full_name='common.ApiRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='secret_key', full_name='common.ApiRequest.secret_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='did', full_name='common.ApiRequest.did', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=69,
)


_APIRESPONSE = _descriptor.Descriptor(
  name='ApiResponse',
  full_name='common.ApiResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='api_key', full_name='common.ApiResponse.api_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_message', full_name='common.ApiResponse.status_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='common.ApiResponse.status', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=71,
  serialized_end=141,
)

DESCRIPTOR.message_types_by_name['ApiRequest'] = _APIREQUEST
DESCRIPTOR.message_types_by_name['ApiResponse'] = _APIRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ApiRequest = _reflection.GeneratedProtocolMessageType('ApiRequest', (_message.Message,), {
  'DESCRIPTOR' : _APIREQUEST,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:common.ApiRequest)
  })
_sym_db.RegisterMessage(ApiRequest)

ApiResponse = _reflection.GeneratedProtocolMessageType('ApiResponse', (_message.Message,), {
  'DESCRIPTOR' : _APIRESPONSE,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:common.ApiResponse)
  })
_sym_db.RegisterMessage(ApiResponse)



_COMMON = _descriptor.ServiceDescriptor(
  name='Common',
  full_name='common.Common',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=143,
  serialized_end=216,
  methods=[
  _descriptor.MethodDescriptor(
    name='GenerateAPIRequest',
    full_name='common.Common.GenerateAPIRequest',
    index=0,
    containing_service=None,
    input_type=_APIREQUEST,
    output_type=_APIRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_COMMON)

DESCRIPTOR.services_by_name['Common'] = _COMMON

# @@protoc_insertion_point(module_scope)