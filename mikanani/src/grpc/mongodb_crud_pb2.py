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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12mongodb_crud.proto\"6\n\x11QueryAnimeRequest\x12\x12\n\nactiveType\x18\x01 \x01(\x05\x12\r\n\x05names\x18\x02 \x03(\t\"3\n\x12QueryAnimeResponse\x12\r\n\x05names\x18\x01 \x03(\t\x12\x0e\n\x06rssUrl\x18\x02 \x03(\t\"Y\n\x12UpdateAnimeRequest\x12\r\n\x05names\x18\x01 \x03(\t\x12\x0e\n\x06rssUrl\x18\x02 \x03(\t\x12\x12\n\nrssVersion\x18\x03 \x03(\t\x12\x10\n\x08rssRegex\x18\x04 \x03(\t\"+\n\x13UpdateAnimeResponse\x12\x14\n\x0csuccessCount\x18\x01 \x01(\x03\" \n\x0f\x44\x65lAnimeRequest\x12\r\n\x05names\x18\x01 \x03(\t\"(\n\x10\x44\x65lAnimeResponse\x12\x14\n\x0csuccessCount\x18\x01 \x01(\x03\x32\xbb\x01\n\x11MikananiMongoCrud\x12\x37\n\nQueryAnime\x12\x12.QueryAnimeRequest\x1a\x13.QueryAnimeResponse\"\x00\x12:\n\x0bUpdateAnime\x12\x13.UpdateAnimeRequest\x1a\x14.UpdateAnimeResponse\"\x00\x12\x31\n\x08\x44\x65lAnime\x12\x10.DelAnimeRequest\x1a\x11.DelAnimeResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mongodb_crud_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_QUERYANIMEREQUEST']._serialized_start=22
  _globals['_QUERYANIMEREQUEST']._serialized_end=76
  _globals['_QUERYANIMERESPONSE']._serialized_start=78
  _globals['_QUERYANIMERESPONSE']._serialized_end=129
  _globals['_UPDATEANIMEREQUEST']._serialized_start=131
  _globals['_UPDATEANIMEREQUEST']._serialized_end=220
  _globals['_UPDATEANIMERESPONSE']._serialized_start=222
  _globals['_UPDATEANIMERESPONSE']._serialized_end=265
  _globals['_DELANIMEREQUEST']._serialized_start=267
  _globals['_DELANIMEREQUEST']._serialized_end=299
  _globals['_DELANIMERESPONSE']._serialized_start=301
  _globals['_DELANIMERESPONSE']._serialized_end=341
  _globals['_MIKANANIMONGOCRUD']._serialized_start=344
  _globals['_MIKANANIMONGOCRUD']._serialized_end=531
# @@protoc_insertion_point(module_scope)
