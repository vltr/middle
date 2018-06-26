import re
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
from typing import _Union

import attr

from .compat import IS_PY37
from .compat import GenericType
from .config import config
from .dtutils import convert_to_utc
from .dtutils import dt_from_iso_string
from .dtutils import dt_from_timestamp
from .exceptions import InvalidType

_num_re = re.compile("^[+-]?([0-9]+([\.][0-9]*)?|[.][0-9]+)$")


def model_converter(model_cls, value):
    if isinstance(value, model_cls):
        return value
    return model_cls(**value)


def _iterable_converter(value_converter, is_set, value):
    res = [value_converter(v) for v in value]
    return res if not is_set else set(res)


def _dict_converter(key_converter, value_converter, value):
    return {key_converter(k): value_converter(v) for k, v in value.items()}


def _str_converter(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return value.decode("utf-8")
    elif config.str_method and hasattr(value, "__str__"):
        return str(value)
    elif config.force_str:
        return str(value)
    raise TypeError(
        'the value "{!s}" given should not be converted to str'.format(value)
    )


def _number_converter(type_, value):
    if isinstance(value, type_):
        return value
    if isinstance(value, str):
        if _num_re.match(value) is not None:
            return type_(value)
    raise TypeError(
        'the value "{!s}" given should not be converted to {}'.format(
            value, type_.__name__
        )
    )


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
        return value.lower().strip() in ("true", "yes", "on", "1")
    elif isinstance(value, (int, float)):
        return value > 0
    elif isinstance(value, bool):
        return value
    raise TypeError(
        'the value "{}" given can\'t be converted to bool'.format(value)
    )


def _multiple_types_converter(converters, value):
    raised_exc = []
    converted_values = []
    # a rough "type-affinity" conversor
    for c in converters:
        try:
            converted_values.append(c(value))
        except TypeError:
            continue
        except Exception as e:
            raised_exc.append(e)

    if raised_exc:
        pass  # TODO do something (?)

    if converted_values:
        if value in converted_values:  # there is a primitive in there
            return value
        else:
            value_type = type(value)
            for cv in converted_values:
                if value_type == type(cv):  # it is the same type (at least)
                    return cv

    return value


def _none_or_converter(converter, value):
    if value is None:
        return None
    return converter(value)


FOR_TYPE = {
    bool: _bool_converter,
    date: _date_converter,
    datetime: _datetime_converter,
    int: partial(_number_converter, int),
    float: partial(_number_converter, float),
    str: _str_converter,
    bytes: _str_converter,
    "MULTIPLE": _multiple_types_converter,
    "NONE_OPT": _none_or_converter,
}


@singledispatch
def converter(type_):
    if type_ in FOR_TYPE:
        return FOR_TYPE[type_]
    elif attr.has(type_):
        return partial(model_converter, type_)
    else:
        print("singledispatch.converter on converters.py")
        from IPython import embed

        embed()
        raise TypeError("SEE ME!")  # TODO


@converter.register(EnumMeta)
def _converter_enum(type_):
    return type_


@converter.register(_Union)
def _converter_union(type_):
    if type_.__args__ is None:
        raise InvalidType(
            "Union must be set with at least two parameters, e.g. Union[int, str]"
        )
    ntype = type(None)
    converter_fns = []
    for arg in type_.__args__:
        if arg == ntype:
            continue
        converter_fns.append(converter(arg))

    if len(converter_fns) == 1:  # only possible is NoneType present
        assert ntype in type_.__args__  # to make sure
        return partial(FOR_TYPE["NONE_OPT"], converter_fns[0])
    else:
        if ntype in type_.__args__:
            return partial(
                FOR_TYPE["NONE_OPT"],
                partial(FOR_TYPE["MULTIPLE"], converter_fns),
            )
        return partial(FOR_TYPE["MULTIPLE"], converter_fns)


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
            raise TypeError("This type is not supported")  # TODO


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
            from IPython import embed

            embed()
            raise TypeError("This type is not supported")  # TODO


# Tuple ?
# Decimal ?
