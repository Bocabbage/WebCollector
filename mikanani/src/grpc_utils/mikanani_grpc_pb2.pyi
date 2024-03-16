from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnimeMeta(_message.Message):
    __slots__ = ("uid", "name", "downloadBitmap", "isActive", "tags")
    UID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADBITMAP_FIELD_NUMBER: _ClassVar[int]
    ISACTIVE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    uid: int
    name: str
    downloadBitmap: int
    isActive: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uid: _Optional[int] = ..., name: _Optional[str] = ..., downloadBitmap: _Optional[int] = ..., isActive: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class AnimeDoc(_message.Message):
    __slots__ = ("uid", "rssUrl", "rule", "regex")
    UID_FIELD_NUMBER: _ClassVar[int]
    RSSURL_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    REGEX_FIELD_NUMBER: _ClassVar[int]
    uid: int
    rssUrl: str
    rule: str
    regex: str
    def __init__(self, uid: _Optional[int] = ..., rssUrl: _Optional[str] = ..., rule: _Optional[str] = ..., regex: _Optional[str] = ...) -> None: ...

class ListAnimeMetaRequest(_message.Message):
    __slots__ = ("startIndex", "endIndex", "statusFilter")
    STARTINDEX_FIELD_NUMBER: _ClassVar[int]
    ENDINDEX_FIELD_NUMBER: _ClassVar[int]
    STATUSFILTER_FIELD_NUMBER: _ClassVar[int]
    startIndex: int
    endIndex: int
    statusFilter: int
    def __init__(self, startIndex: _Optional[int] = ..., endIndex: _Optional[int] = ..., statusFilter: _Optional[int] = ...) -> None: ...

class ListAnimeMetaResponse(_message.Message):
    __slots__ = ("itemCount", "animeMetas")
    ITEMCOUNT_FIELD_NUMBER: _ClassVar[int]
    ANIMEMETAS_FIELD_NUMBER: _ClassVar[int]
    itemCount: int
    animeMetas: _containers.RepeatedCompositeFieldContainer[AnimeMeta]
    def __init__(self, itemCount: _Optional[int] = ..., animeMetas: _Optional[_Iterable[_Union[AnimeMeta, _Mapping]]] = ...) -> None: ...

class GetAnimeDocRequest(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: int
    def __init__(self, uid: _Optional[int] = ...) -> None: ...

class GetAnimeDocResponse(_message.Message):
    __slots__ = ("animeDoc",)
    ANIMEDOC_FIELD_NUMBER: _ClassVar[int]
    animeDoc: AnimeDoc
    def __init__(self, animeDoc: _Optional[_Union[AnimeDoc, _Mapping]] = ...) -> None: ...

class UpdateAnimeDocRequest(_message.Message):
    __slots__ = ("updateAnimeDoc",)
    UPDATEANIMEDOC_FIELD_NUMBER: _ClassVar[int]
    updateAnimeDoc: AnimeDoc
    def __init__(self, updateAnimeDoc: _Optional[_Union[AnimeDoc, _Mapping]] = ...) -> None: ...

class UpdateAnimeMetaRequest(_message.Message):
    __slots__ = ("updateAnimeMeta",)
    UPDATEANIMEMETA_FIELD_NUMBER: _ClassVar[int]
    updateAnimeMeta: AnimeMeta
    def __init__(self, updateAnimeMeta: _Optional[_Union[AnimeMeta, _Mapping]] = ...) -> None: ...

class InsertAnimeItemRequest(_message.Message):
    __slots__ = ("insertAnimeMeta", "insertAnimeDoc")
    INSERTANIMEMETA_FIELD_NUMBER: _ClassVar[int]
    INSERTANIMEDOC_FIELD_NUMBER: _ClassVar[int]
    insertAnimeMeta: AnimeMeta
    insertAnimeDoc: AnimeDoc
    def __init__(self, insertAnimeMeta: _Optional[_Union[AnimeMeta, _Mapping]] = ..., insertAnimeDoc: _Optional[_Union[AnimeDoc, _Mapping]] = ...) -> None: ...

class DeleteAnimeItemRequest(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: int
    def __init__(self, uid: _Optional[int] = ...) -> None: ...
