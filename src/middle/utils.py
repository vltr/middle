from datetime import date
from datetime import datetime
from enum import EnumMeta
from functools import lru_cache
from functools import singledispatch
from typing import Collection
from typing import Dict
from typing import FrozenSet
from typing import Iterable
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import Sequence
from typing import Set

import attr

from .compat import IS_PY37
from .compat import GenericType
from .dtutils import dt_to_iso_string
from .schema import ModelMeta


def asdict(inst):
    return {
        f.name: _raw_value(f.type)(getattr(inst, f.name))
        for f in attr.fields(inst.__class__)
    }


def _raw_primitive(value):
    if isinstance(value, date):
        return value.isoformat()
    elif isinstance(value, datetime):
        # return dt_to_iso_string(convert_to_utc(value))
        return dt_to_iso_string(value)
    return value


# def _raw_date_datetime(value):
#     return value.isoformat()


def _raw_enum(value):
    return value.value


def _raw_model_meta(value):
    return asdict(value)


def _raw_list(value):
    return [_raw_value(type(v))(v) for v in value]


def _raw_set(value):
    return {_raw_value(type(v))(v) for v in value}


# def _raw_tuple(value):
#     return (_raw_value(v)(v) for v in value)


def _raw_dict(value):
    return {
        _raw_value(type(k))(k): _raw_value(type(v))(v)
        for k, v in value.items()
    }


@lru_cache(typed=True)
@singledispatch
def _raw_value(type_):
    return _raw_primitive


# @_raw_value.register(date)
# @_raw_value.register(datetime)
# def _raw_value_datetime(type_):
#     return _raw_date_datetime


@_raw_value.register(EnumMeta)
def _raw_value_enum(type_):
    return _raw_enum


@_raw_value.register(ModelMeta)
def _raw_value_model_meta(type_):
    return _raw_model_meta


if IS_PY37:
    @_raw_value.register(GenericType)
    def _raw_value_generic_meta(type_):
        if type_._name in (
            "List",
            "Sequence",
            "Collection",
            "Iterable",
            "MutableSequence",
        ):
            return _raw_list
        elif type_._name in ("Set", "MutableSet", "FrozenSet"):
            return _raw_set
        # elif type_._name == Tuple:
        #     return _raw_tuple
        elif type_._name in ("Dict", "Mapping", "MutableMapping"):
            return _raw_dict
        else:
            print("utils.py")
            # from IPython import embed

            # embed()
            raise TypeError("This type is not supported")
else:
    @_raw_value.register(GenericType)
    def _raw_value_generic_meta(type_):
        if type_.__base__ in (
            List,
            Sequence,
            Collection,
            Iterable,
            MutableSequence,
        ):
            return _raw_list
        elif type_.__base__ in (Set, MutableSet, FrozenSet):
            return _raw_set
        # elif type_.__base__ == Tuple:
        #     return _raw_tuple
        elif type_.__base__ in (Dict, Mapping, MutableMapping):
            return _raw_dict
        else:
            print("utils.py")
            # from IPython import embed

            # embed()
            raise TypeError("This type is not supported")
