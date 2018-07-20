import re
import sys
import typing
from datetime import date
from datetime import datetime
from decimal import Decimal
from enum import EnumMeta
from functools import lru_cache

_IS_PY36 = False
RegexPatternType = None
if sys.version_info[:2] >= (3, 7):
    from typing import _GenericAlias as GenericType

    RegexPatternType = re.Pattern
else:
    from typing import GenericMeta as GenericType

    RegexPatternType = re._pattern_type

    _IS_PY36 = True


TypeRegistry = {}
NoneType = type(None)


@lru_cache(maxsize=None)
def get_type(type_):
    if type_ is None:
        return NoneType
    if type_ in (
        str,
        int,
        float,
        bool,
        bytes,
        date,
        datetime,
        Decimal,
        typing.Dict,
        typing.List,
        typing.Set,
        typing.Tuple,
        typing.Union,
    ):
        return type_

    tt = type(type_)
    if tt == type:
        tt = type_
    if hasattr(type_, "__origin__") or isinstance(tt, GenericType):
        if _IS_PY36:  # py36
            return type_.__origin__
        else:  # py37
            if hasattr(type_, "_name") and isinstance(type_._name, str):
                return getattr(typing, type_._name)
            return type_.__origin__
    elif tt == EnumMeta:
        return tt
    elif tt in TypeRegistry:
        return TypeRegistry[tt]
    return type_


__all__ = ("get_type", "NoneType", "RegexPatternType", "TypeRegistry")
