# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: storage.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rstorage.proto\x12\x07storage\"-\n\x1aSpecializationGroupRequest\x12\x0f\n\x07habr_id\x18\x01 \x01(\x03\"Y\n\x1bSpecializationGroupResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07name_en\x18\x03 \x01(\t\x12\x0f\n\x07habr_id\x18\x04 \x01(\x03\x32p\n\x07Storage\x12\x65\n\x16GetSpecializationGroup\x12#.storage.SpecializationGroupRequest\x1a$.storage.SpecializationGroupResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'storage_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SPECIALIZATIONGROUPREQUEST']._serialized_start=26
  _globals['_SPECIALIZATIONGROUPREQUEST']._serialized_end=71
  _globals['_SPECIALIZATIONGROUPRESPONSE']._serialized_start=73
  _globals['_SPECIALIZATIONGROUPRESPONSE']._serialized_end=162
  _globals['_STORAGE']._serialized_start=164
  _globals['_STORAGE']._serialized_end=276
# @@protoc_insertion_point(module_scope)
