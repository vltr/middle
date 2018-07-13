import datetime
import typing
from decimal import Decimal
from enum import EnumMeta

import attr

from .compat import get_type
from .dispatch import type_dispatch
from .dtutils import dt_to_iso_string


def asdict(inst):
    return {
        f.name: value_of(f.type)(getattr(inst, f.name))
        for f in attr.fields(inst.__class__)
    }


def _raw_primitive(value):
    return value


def _raw_decimal(value):
    return float(value)


def _raw_date(value):
    return value.isoformat()


def _raw_datetime(value):
    return dt_to_iso_string(value)


def _raw_enum(value):
    return value.value


def _raw_list(value):
    return [value_of(get_type(v))(v) for v in value]


def _raw_set(value):
    return {value_of(get_type(v))(v) for v in value}


def _raw_tuple(value):
    return tuple(value_of(get_type(v))(v) for v in value)


def _raw_dict(value):
    return {
        value_of(get_type(k))(k): value_of(type(v))(v)
        for k, v in value.items()
    }


@type_dispatch(lru=True)
def value_of(type_):
    if attr.has(type_):
        return asdict
    return _raw_primitive


@value_of.register(Decimal)
def _value_of_decimal(type_):
    return _raw_decimal


@value_of.register(datetime.date)
def _value_of_date(type_):
    return _raw_date


@value_of.register(datetime.datetime)
def _value_of_datetime(type_):
    return _raw_datetime


@value_of.register(EnumMeta)
def _value_of_enum(type_):
    return _raw_enum


@value_of.register(typing.List)
def _value_of_list(type_):
    return _raw_list


@value_of.register(typing.Set)
def _value_of_set(type_):
    return _raw_set


@value_of.register(typing.Dict)
def _value_of_dict(type_):
    return _raw_dict


@value_of.register(typing.Tuple)
def _value_of_tuple(type_):
    return _raw_tuple
