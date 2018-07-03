import sys
import typing
from datetime import date
from datetime import datetime
from decimal import Decimal
from enum import EnumMeta

IS_PY36 = False
if sys.version_info >= (3, 7):
    from typing import _GenericAlias as GenericType
else:
    from typing import GenericMeta as GenericType

    IS_PY36 = True


TYPE_REGISTRY = {}
NONETYPE = type(None)


def get_type(type_):
    if type_ is None:
        return NONETYPE
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
        typing.Collection,
        typing.Iterable,
        typing.Sequence,
        typing.MutableSequence,
        typing.FrozenSet,
        typing.MutableSet,
        typing.Mapping,
        typing.MutableMapping,
    ):
        return type_

    tt = type(type_)
    if tt == type:
        tt = type_
    if hasattr(type_, "__origin__") or isinstance(tt, GenericType):
        if IS_PY36:  # py36
            return type_.__origin__
        else:  # py37
            if hasattr(type_, "_name") and isinstance(type_._name, str):
                return getattr(typing, type_._name)
            return type_.__origin__
    elif tt == EnumMeta:
        return tt
    elif tt in TYPE_REGISTRY:
        return TYPE_REGISTRY[tt]
    return type_
