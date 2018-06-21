from datetime import date
from datetime import datetime
from enum import EnumMeta
from functools import partial
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
from .dtutils import convert_to_utc
from .dtutils import dt_from_iso_string
from .dtutils import dt_from_timestamp


def model_converter(model_cls, value):
    if isinstance(value, model_cls):
        return value
    return model_cls(**value)


def _iterable_converter(value_converter, is_set, value):
    res = [value_converter(v) for v in value]
    return res if not is_set else set(res)


def _dict_converter(key_converter, value_converter, value):
    return {key_converter(k): value_converter(v) for k, v in value.items()}


def _date_converter(value):
    if isinstance(value, date):
        return value
    elif isinstance(value, str):
        return dt_from_iso_string(value).date()
    elif isinstance(value, (tuple, list)) and len(value) > 2:
        return date(*value[:3])
    elif isinstance(value, (int, float)):
        return date.fromtimestamp(value)
    raise TypeError(
        'the value "{}" given can\'t be converted to date'.format(value)
    )


def _datetime_converter(value):
    if isinstance(value, datetime):
        return value
    elif isinstance(value, str):
        return dt_from_iso_string(value)
    elif isinstance(value, (tuple, list)) and len(value) > 2:
        return convert_to_utc(datetime(*value))
    elif isinstance(value, (int, float)):
        return dt_from_timestamp(value)
    raise TypeError(
        'the value "{}" given can\'t be converted to datetime'.format(value)
    )


def _bool_converter(value):
    if isinstance(value, str):
        return value.lower() in ("true", "yes")
    elif isinstance(value, (int, float)):
        return value > 0
    elif isinstance(value, bool):
        return value
    raise TypeError(
        'the value "{}" given can\'t be converted to bool'.format(value)
    )


@singledispatch
def converter(type_):
    if type_ in (int, float, str):
        return type_
    elif type_ == bool:
        return _bool_converter
    elif type_ == date:
        return _date_converter
    elif type_ == datetime:
        return _datetime_converter
    elif attr.has(type_):
        return partial(model_converter, type_)
    else:
        raise TypeError("SEE ME!")


@converter.register(EnumMeta)
def _converter_enum(type_):
    return type_


if IS_PY37:
    @converter.register(GenericType)
    def _converter_generic_meta(type_):
        if type_._name in (
            "List",
            "Set",
            "MutableSet",
            "Sequence",
            "Collection",
            "Iterable",
            "MutableSequence",
            "FrozenSet",
        ):
            if type_.__args__:
                return partial(
                    _iterable_converter,
                    converter(type_.__args__[0]),
                    type_._name in ("Set", "MutableSet", "FrozenSet"),
                )
        elif type_._name in ("Dict", "Mapping", "MutableMapping"):
            if type_.__args__:
                return partial(
                    _dict_converter,
                    converter(type_.__args__[0]),
                    converter(type_.__args__[1]),
                )
        else:
            print("converters.py")
            # from IPython import embed

            # embed()
            raise TypeError("This type is not supported")
else:
    @converter.register(GenericType)
    def _converter_generic_meta(type_):
        if type_.__base__ in (
            List,
            Set,
            MutableSet,
            Sequence,
            Collection,
            Iterable,
            MutableSequence,
            FrozenSet,
        ):
            if type_.__args__:
                return partial(
                    _iterable_converter,
                    converter(type_.__args__[0]),
                    type_.__base__ in (Set, MutableSet, FrozenSet),
                )
        elif type_.__base__ in (Dict, Mapping, MutableMapping):
            if type_.__args__:
                return partial(
                    _dict_converter,
                    converter(type_.__args__[0]),
                    converter(type_.__args__[1]),
                )
        else:
            print("converters.py")
            # from IPython import embed

            # embed()
            raise TypeError("This type is not supported")


# List, MutableSequence, Sequence, Collection, Iterable
# Dict, MutableMapping, Mapping
# MutableSet, Set, FrozenSet
# Any, Optional, Union <<<
# Tuple ?
# Decimal ?
