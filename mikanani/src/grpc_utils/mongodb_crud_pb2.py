# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mongodb_crud.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12mongodb_crud.proto\x12\x13mikanani_grpc_utils\"6\n\x11QueryAnimeRequest\x12\x12\n\nactiveType\x18\x01 \x01(\x05\x12\r\n\x05names\x18\x02 \x03(\t\"3\n\x12QueryAnimeResponse\x12\r\n\x05names\x18\x02 \x03(\t\x12\x0e\n\x06rssUrl\x18\x03 \x03(\t\"q\n\x12UpdateAnimeRequest\x12\r\n\x05names\x18\x02 \x03(\t\x12\x0f\n\x07rssUrls\x18\x03 \x03(\t\x12\x14\n\x0cruleVersions\x18\x04 \x03(\t\x12\x12\n\nruleRegexs\x18\x05 \x03(\t\x12\x11\n\tisActives\x18\x06 \x03(\x08\"?\n\x13UpdateAnimeResponse\x12\x14\n\x0csuccessCount\x18\x01 \x01(\x03\x12\x12\n\nfailedList\x18\x02 \x03(\t\"0\n\x0f\x44\x65lAnimeRequest\x12\x0e\n\x06\x64\x65lAll\x18\x01 \x01(\x08\x12\r\n\x05names\x18\x02 \x03(\t\"(\n\x10\x44\x65lAnimeResponse\x12\x14\n\x0csuccessCount\x18\x01 \x01(\x03\x32\xb3\x02\n\x11MikananiMongoCrud\x12_\n\nQueryAnime\x12&.mikanani_grpc_utils.QueryAnimeRequest\x1a\'.mikanani_grpc_utils.QueryAnimeResponse\"\x00\x12\x62\n\x0bUpdateAnime\x12\'.mikanani_grpc_utils.UpdateAnimeRequest\x1a(.mikanani_grpc_utils.UpdateAnimeResponse\"\x00\x12Y\n\x08\x44\x65lAnime\x12$.mikanani_grpc_utils.DelAnimeRequest\x1a%.mikanani_grpc_utils.DelAnimeResponse\"\x00\x42\x17Z\x15./internal/grpc_utilsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mongodb_crud_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\025./internal/grpc_utils'
  _globals['_QUERYANIMEREQUEST']._serialized_start=43
  _globals['_QUERYANIMEREQUEST']._serialized_end=97
  _globals['_QUERYANIMERESPONSE']._serialized_start=99
  _globals['_QUERYANIMERESPONSE']._serialized_end=150
  _globals['_UPDATEANIMEREQUEST']._serialized_start=152
  _globals['_UPDATEANIMEREQUEST']._serialized_end=265
  _globals['_UPDATEANIMERESPONSE']._serialized_start=267
  _globals['_UPDATEANIMERESPONSE']._serialized_end=330
  _globals['_DELANIMEREQUEST']._serialized_start=332
  _globals['_DELANIMEREQUEST']._serialized_end=380
  _globals['_DELANIMERESPONSE']._serialized_start=382
  _globals['_DELANIMERESPONSE']._serialized_end=422
  _globals['_MIKANANIMONGOCRUD']._serialized_start=425
  _globals['_MIKANANIMONGOCRUD']._serialized_end=732
# @@protoc_insertion_point(module_scope)