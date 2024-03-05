from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class QueryAnimeRequest(_message.Message):
    __slots__ = ("activeType", "names")
    ACTIVETYPE_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    activeType: int
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, activeType: _Optional[int] = ..., names: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryAnimeResponse(_message.Message):
    __slots__ = ("ids", "names", "rssUrl")
    IDS_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    RSSURL_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    rssUrl: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., names: _Optional[_Iterable[str]] = ..., rssUrl: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateAnimeRequest(_message.Message):
    __slots__ = ("ids", "names", "rssUrls", "rssVersions", "rssRegexs", "isActives")
    IDS_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    RSSURLS_FIELD_NUMBER: _ClassVar[int]
    RSSVERSIONS_FIELD_NUMBER: _ClassVar[int]
    RSSREGEXS_FIELD_NUMBER: _ClassVar[int]
    ISACTIVES_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    rssUrls: _containers.RepeatedScalarFieldContainer[str]
    rssVersions: _containers.RepeatedScalarFieldContainer[str]
    rssRegexs: _containers.RepeatedScalarFieldContainer[str]
    isActives: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., names: _Optional[_Iterable[str]] = ..., rssUrls: _Optional[_Iterable[str]] = ..., rssVersions: _Optional[_Iterable[str]] = ..., rssRegexs: _Optional[_Iterable[str]] = ..., isActives: _Optional[_Iterable[bool]] = ...) -> None: ...

class UpdateAnimeResponse(_message.Message):
    __slots__ = ("successCount", "failedList")
    SUCCESSCOUNT_FIELD_NUMBER: _ClassVar[int]
    FAILEDLIST_FIELD_NUMBER: _ClassVar[int]
    successCount: int
    failedList: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, successCount: _Optional[int] = ..., failedList: _Optional[_Iterable[str]] = ...) -> None: ...

class DelAnimeRequest(_message.Message):
    __slots__ = ("delAll", "ids")
    DELALL_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    delAll: bool
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, delAll: bool = ..., ids: _Optional[_Iterable[int]] = ...) -> None: ...

class DelAnimeResponse(_message.Message):
    __slots__ = ("successCount", "failedList")
    SUCCESSCOUNT_FIELD_NUMBER: _ClassVar[int]
    FAILEDLIST_FIELD_NUMBER: _ClassVar[int]
    successCount: int
    failedList: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, successCount: _Optional[int] = ..., failedList: _Optional[_Iterable[str]] = ...) -> None: ...
