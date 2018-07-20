import datetime
import typing
from decimal import Decimal
from enum import EnumMeta
from functools import partial

import attr

from ..compat import NoneType
from ..dispatch import type_dispatch
from .dicts import DictValidator
from .lists import ListValidator
from .numbers import NumberValidator
from .strings import StringValidator


def _complex_validator(validator_cls, sub_type, type_, field):
    validators = []
    if validator_cls is not None:
        kwargs = {}
        for key in validator_cls.validator_keys():
            if key in field.metadata:
                kwargs.update({key: field.metadata.get(key)})
        if kwargs:
            validators.append(validator_cls(**kwargs))
    validators.append(
        attr.validators.instance_of(_get_instances_of(sub_type, field))
    )
    return validators


_generic_fn = partial(_complex_validator, None)
_str_fn = partial(_complex_validator, StringValidator)
_num_fn = partial(_complex_validator, NumberValidator)
_list_fn = partial(_complex_validator, ListValidator, list)
_set_fn = partial(_complex_validator, ListValidator, set)
_dict_fn = partial(_complex_validator, DictValidator, dict)


def _get_instances_of(type_, field):
    if field._default is None:
        return (type_, NoneType)
    return type_


@type_dispatch()
def validate(type_, field):
    return []


@validate.register(str)
def _apply_str(type_, field):
    return _str_fn(type_, type_, field)


@validate.register(int)
@validate.register(float)
@validate.register(Decimal)
def _apply_number(type_, field):
    return _num_fn(type_, type_, field)


@validate.register(bool)
@validate.register(datetime.date)
@validate.register(datetime.datetime)
@validate.register(EnumMeta)
def _apply_bool_dt_dttime_enum(type_, field):
    return _generic_fn(type_, type_, field)


@validate.register(typing.List)
def _validate_list(type_, field):
    return _list_fn(type_, field)


@validate.register(typing.Set)
def _validate_set(type_, field):
    return _set_fn(type_, field)


@validate.register(typing.Dict)
def _validate_dict(type_, field):
    return _dict_fn(type_, field)


@validate.register(typing.Union)
def _validate_union(type_, field):
    validator_types = []
    for arg in type_.__args__:
        if arg == NoneType:
            validator_types.append(NoneType)
        else:
            if arg in (
                str,
                int,
                float,
                bool,
                datetime.date,
                datetime.datetime,
                list,
                dict,
            ):
                validator_types.append(arg)
            elif attr.has(arg):
                validator_types.append(arg)

    return [attr.validators.instance_of(tuple(validator_types))]
