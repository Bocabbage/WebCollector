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
    __slots__ = ("names", "rssUrl")
    NAMES_FIELD_NUMBER: _ClassVar[int]
    RSSURL_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    rssUrl: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ..., rssUrl: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateAnimeRequest(_message.Message):
    __slots__ = ("names", "rssUrl", "rssVersion", "rssRegex")
    NAMES_FIELD_NUMBER: _ClassVar[int]
    RSSURL_FIELD_NUMBER: _ClassVar[int]
    RSSVERSION_FIELD_NUMBER: _ClassVar[int]
    RSSREGEX_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    rssUrl: _containers.RepeatedScalarFieldContainer[str]
    rssVersion: _containers.RepeatedScalarFieldContainer[str]
    rssRegex: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ..., rssUrl: _Optional[_Iterable[str]] = ..., rssVersion: _Optional[_Iterable[str]] = ..., rssRegex: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateAnimeResponse(_message.Message):
    __slots__ = ("successCount",)
    SUCCESSCOUNT_FIELD_NUMBER: _ClassVar[int]
    successCount: int
    def __init__(self, successCount: _Optional[int] = ...) -> None: ...

class DelAnimeRequest(_message.Message):
    __slots__ = ("names",)
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...

class DelAnimeResponse(_message.Message):
    __slots__ = ("successCount",)
    SUCCESSCOUNT_FIELD_NUMBER: _ClassVar[int]
    successCount: int
    def __init__(self, successCount: _Optional[int] = ...) -> None: ...
