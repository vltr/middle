import datetime
import typing
from decimal import Decimal
from enum import EnumMeta

import attr

from ..compat import NoneType
from ..dispatch import type_dispatch
from .dicts import DictValidator
from .lists import ListValidator
from .numbers import NumberValidator
from .strings import StringValidator


def _get_instances_of(type_, field):
    if field._default is None:
        return (type_, NoneType)
    return type_


@type_dispatch()
def validate(type_, field):
    return []


@validate.register(str)
def _apply_str(type_, field):
    validators = []
    kwargs = {}
    for key in StringValidator.validator_keys():
        if key in field.metadata:
            kwargs.update({key: field.metadata.get(key)})
    if kwargs:
        validators.append(StringValidator(**kwargs))
    validators.append(
        attr.validators.instance_of(_get_instances_of(type_, field))
    )
    return validators


@validate.register(int)
@validate.register(float)
@validate.register(Decimal)
def _apply_number(type_, field):
    validators = []
    kwargs = {}
    for key in NumberValidator.validator_keys():
        if key in field.metadata:
            kwargs.update({key: field.metadata.get(key)})
    if kwargs:
        validators.append(NumberValidator(**kwargs))
    validators.append(
        attr.validators.instance_of(_get_instances_of(type_, field))
    )
    return validators


@validate.register(bool)
@validate.register(datetime.date)
@validate.register(datetime.datetime)
def _apply_bool_dt_dttime(type_, field):
    return [attr.validators.instance_of(_get_instances_of(type_, field))]


@validate.register(EnumMeta)
def _validate_enum(type_, field):
    return [attr.validators.instance_of(_get_instances_of(type_, field))]


@validate.register(typing.List)
def _validate_list(type_, field):
    validators = []
    kwargs = {}
    for key in ListValidator.validator_keys():
        if key in field.metadata:
            kwargs.update({key: field.metadata.get(key)})
    if kwargs:
        validators.append(ListValidator(**kwargs))
    validators.append(
        attr.validators.instance_of(_get_instances_of(list, field))
    )
    return validators


@validate.register(typing.Set)
def _validate_set(type_, field):
    validators = []
    kwargs = {}
    for key in ListValidator.validator_keys():
        if key in field.metadata:
            kwargs.update({key: field.metadata.get(key)})
    if kwargs:
        validators.append(ListValidator(**kwargs))
    validators.append(
        attr.validators.instance_of(_get_instances_of(set, field))
    )
    return validators


@validate.register(typing.Dict)
def _validate_dict(type_, field):
    validators = []
    kwargs = {}
    for key in DictValidator.validator_keys():
        if key in field.metadata:
            kwargs.update({key: field.metadata.get(key)})
    if kwargs:
        validators.append(DictValidator(**kwargs))
    validators.append(
        attr.validators.instance_of(_get_instances_of(dict, field))
    )
    return validators


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
