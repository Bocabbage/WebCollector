# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mikanani_grpc.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13mikanani_grpc.proto\x12\x13mikanani_grpc_utils\x1a\x1bgoogle/protobuf/empty.proto\"^\n\tAnimeMeta\x12\x0b\n\x03uid\x18\x01 \x01(\x03\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0e\x64ownloadBitmap\x18\x03 \x01(\x03\x12\x10\n\x08isActive\x18\x04 \x01(\x05\x12\x0c\n\x04tags\x18\x05 \x03(\t\"D\n\x08\x41nimeDoc\x12\x0b\n\x03uid\x18\x01 \x01(\x03\x12\x0e\n\x06rssUrl\x18\x02 \x01(\t\x12\x0c\n\x04rule\x18\x03 \x01(\t\x12\r\n\x05regex\x18\x04 \x01(\t\"R\n\x14ListAnimeMetaRequest\x12\x12\n\nstartIndex\x18\x01 \x01(\x03\x12\x10\n\x08\x65ndIndex\x18\x02 \x01(\x03\x12\x14\n\x0cstatusFilter\x18\x03 \x01(\x05\"^\n\x15ListAnimeMetaResponse\x12\x11\n\titemCount\x18\x01 \x01(\x03\x12\x32\n\nanimeMetas\x18\x02 \x03(\x0b\x32\x1e.mikanani_grpc_utils.AnimeMeta\"!\n\x12GetAnimeDocRequest\x12\x0b\n\x03uid\x18\x01 \x01(\x03\"F\n\x13GetAnimeDocResponse\x12/\n\x08\x61nimeDoc\x18\x01 \x01(\x0b\x32\x1d.mikanani_grpc_utils.AnimeDoc\"N\n\x15UpdateAnimeDocRequest\x12\x35\n\x0eupdateAnimeDoc\x18\x01 \x01(\x0b\x32\x1d.mikanani_grpc_utils.AnimeDoc\"Q\n\x16UpdateAnimeMetaRequest\x12\x37\n\x0fupdateAnimeMeta\x18\x01 \x01(\x0b\x32\x1e.mikanani_grpc_utils.AnimeMeta\"\x88\x01\n\x16InsertAnimeItemRequest\x12\x37\n\x0finsertAnimeMeta\x18\x01 \x01(\x0b\x32\x1e.mikanani_grpc_utils.AnimeMeta\x12\x35\n\x0einsertAnimeDoc\x18\x02 \x01(\x0b\x32\x1d.mikanani_grpc_utils.AnimeDoc\"%\n\x16\x44\x65leteAnimeItemRequest\x12\x0b\n\x03uid\x18\x01 \x01(\x03\x32\x8f\x05\n\x0fMikananiService\x12h\n\rListAnimeMeta\x12).mikanani_grpc_utils.ListAnimeMetaRequest\x1a*.mikanani_grpc_utils.ListAnimeMetaResponse\"\x00\x12\x62\n\x0bGetAnimeDoc\x12\'.mikanani_grpc_utils.GetAnimeDocRequest\x1a(.mikanani_grpc_utils.GetAnimeDocResponse\"\x00\x12V\n\x0eUpdateAnimeDoc\x12*.mikanani_grpc_utils.UpdateAnimeDocRequest\x1a\x16.google.protobuf.Empty\"\x00\x12X\n\x0fUpdateAnimeMeta\x12+.mikanani_grpc_utils.UpdateAnimeMetaRequest\x1a\x16.google.protobuf.Empty\"\x00\x12X\n\x0fInsertAnimeItem\x12+.mikanani_grpc_utils.InsertAnimeItemRequest\x1a\x16.google.protobuf.Empty\"\x00\x12X\n\x0f\x44\x65leteAnimeItem\x12+.mikanani_grpc_utils.DeleteAnimeItemRequest\x1a\x16.google.protobuf.Empty\"\x00\x12H\n\x14\x44ispatchDownloadTask\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x42 Z\x1e./internal/mikanani_grpc_utilsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mikanani_grpc_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\036./internal/mikanani_grpc_utils'
  _globals['_ANIMEMETA']._serialized_start=73
  _globals['_ANIMEMETA']._serialized_end=167
  _globals['_ANIMEDOC']._serialized_start=169
  _globals['_ANIMEDOC']._serialized_end=237
  _globals['_LISTANIMEMETAREQUEST']._serialized_start=239
  _globals['_LISTANIMEMETAREQUEST']._serialized_end=321
  _globals['_LISTANIMEMETARESPONSE']._serialized_start=323
  _globals['_LISTANIMEMETARESPONSE']._serialized_end=417
  _globals['_GETANIMEDOCREQUEST']._serialized_start=419
  _globals['_GETANIMEDOCREQUEST']._serialized_end=452
  _globals['_GETANIMEDOCRESPONSE']._serialized_start=454
  _globals['_GETANIMEDOCRESPONSE']._serialized_end=524
  _globals['_UPDATEANIMEDOCREQUEST']._serialized_start=526
  _globals['_UPDATEANIMEDOCREQUEST']._serialized_end=604
  _globals['_UPDATEANIMEMETAREQUEST']._serialized_start=606
  _globals['_UPDATEANIMEMETAREQUEST']._serialized_end=687
  _globals['_INSERTANIMEITEMREQUEST']._serialized_start=690
  _globals['_INSERTANIMEITEMREQUEST']._serialized_end=826
  _globals['_DELETEANIMEITEMREQUEST']._serialized_start=828
  _globals['_DELETEANIMEITEMREQUEST']._serialized_end=865
  _globals['_MIKANANISERVICE']._serialized_start=868
  _globals['_MIKANANISERVICE']._serialized_end=1523
# @@protoc_insertion_point(module_scope)
