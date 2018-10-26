import datetime
import re
import typing
from decimal import Decimal
from enum import EnumMeta
from functools import partial

import attr

from .compat import NoneType
from .config import config
from .dispatch import type_dispatch
from .dtutils import dt_convert_to_utc
from .dtutils import dt_from_iso_string
from .dtutils import dt_from_timestamp
from .exceptions import InvalidType

_num_re = re.compile(r"^[+-]?([0-9]+([\.][0-9]*)?|[.][0-9]+)$")


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
    if isinstance(value, datetime.date):
        return value
    elif isinstance(value, str):
        return dt_from_iso_string(value).date()
    elif isinstance(value, (tuple, list)) and len(value) > 2:
        return datetime.date(*value[:3])
    elif isinstance(value, (int, float)):
        return datetime.date.fromtimestamp(value)
    raise TypeError(
        'the value "{}" given can\'t be converted to date'.format(value)
    )


def _datetime_converter(value):
    if isinstance(value, datetime.datetime):
        return dt_convert_to_utc(value)
    elif isinstance(value, str):
        dt = dt_from_iso_string(value)
        return dt_convert_to_utc(dt)
    elif isinstance(value, (tuple, list)) and 2 <= len(value) < 9:
        if len(value) == 8:  # we have a tz offset (TODO document, hours only)
            tz = datetime.timezone(datetime.timedelta(hours=value[7]))
            dt = datetime.datetime(*value[:7], tzinfo=tz)
            return dt_convert_to_utc(dt)
        else:
            return dt_convert_to_utc(datetime.datetime(*value))
    elif isinstance(value, (int, float)):
        return dt_from_timestamp(value)
    raise TypeError(
        'the value "{}" given can\'t be converted to datetime'.format(value)
    )


def _bool_converter(value):
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return value.lower().strip() in ("true", "yes", "on", "1")
    elif isinstance(value, (int, float)):
        return value > 0
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

    if raised_exc:
        pass  # TODO do something (?)

    if converted_values:
        if value in converted_values:  # there is a primitive in there
            return value
        else:  # will this part ever be used?
            value_type = type(value)
            for cv in converted_values:
                if value_type == type(cv):  # it is the same type (at least)
                    return cv

    return value


def _multiple_types_converter_ordered(converters, value):
    converted_values = []
    if len(converters) != len(value):
        raise ValueError(
            "the given value for Tuple doesn't match the size declared"
        )
    for c, v in zip(converters, value):
        converted_values.append(c(v))
    return tuple(converted_values)


def _none_or_converter(converter, value):
    return converter(value)


@type_dispatch(lru=True)
def converter(type_):
    if attr.has(type_):
        return partial(model_converter, type_)
    else:
        raise InvalidType()


@converter.register(NoneType)
def _converter_none(type_):
    return partial(_none_or_converter, lambda _: None)


@converter.register(str)
@converter.register(bytes)
def _converter_str(type_):
    return _str_converter


@converter.register(int)
@converter.register(float)
@converter.register(Decimal)
def _converter_number(type_):
    return partial(_number_converter, type_)


@converter.register(bool)
def _converter_bool(type_):
    return _bool_converter


@converter.register(datetime.date)
def _converter_date(type_):
    return _date_converter


@converter.register(datetime.datetime)
def _converter_datetime(type_):
    return _datetime_converter


@converter.register(EnumMeta)
def _converter_enum(type_):
    return type_


@converter.register(typing.List)
def _converter_iterable_list(type_):
    if not type_.__args__:
        raise InvalidType(
            "{0!r} must be set with only one parameter, e.g. {0!r}[float]".format(
                type_
            )
        )
    return partial(_iterable_converter, converter(type_.__args__[0]), False)


@converter.register(typing.Set)
def _converter_iterable_set(type_):
    if not type_.__args__:
        raise InvalidType(
            "{0!r} must be set with only one parameter, e.g. {0!r}[float]".format(
                type_
            )
        )
    return partial(_iterable_converter, converter(type_.__args__[0]), True)


@converter.register(typing.Dict)
def _converter_dict(type_):
    if not type_.__args__:
        raise InvalidType(
            "{0!r} must be set with parameters, e.g. {0!r}[str, str]".format(
                type_
            )
        )
    return partial(
        _dict_converter,
        converter(type_.__args__[0]),
        converter(type_.__args__[1]),
    )


@converter.register(typing.Union)
def _converter_union(type_):
    if not hasattr(type_, "__args__") or not type_.__args__:
        raise InvalidType(
            "Union must be set with at least two parameters, e.g. Union[int, str]"
        )
    converter_fns = []
    for arg in type_.__args__:
        if arg == NoneType:
            continue
        converter_fns.append(converter(arg))

    if len(converter_fns) == 1:  # only possible is NoneType present
        if NoneType not in type_.__args__:  # noqa
            raise TypeError(
                "There should be None inside with the usage of Optional"
            )
        return partial(_none_or_converter, converter_fns[0])
    else:
        if NoneType in type_.__args__:
            return partial(
                _none_or_converter,
                partial(_multiple_types_converter, converter_fns),
            )
        return partial(_multiple_types_converter, converter_fns)


@converter.register(typing.Tuple)
def _converter_tuple(type_):
    if not type_.__args__:
        raise InvalidType(
            "Tuple must be set with at least one parameters, e.g. Tuple[bool]"
        )
    return partial(
        _multiple_types_converter_ordered,
        [converter(arg) for arg in type_.__args__],
    )
