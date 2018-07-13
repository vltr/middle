import datetime
import typing
from decimal import Decimal
from enum import EnumMeta
from functools import partial

import attr

from ..compat import NONETYPE
from ..dispatch import type_dispatch
from .common import FOR_TYPE


def _append_to(validators, metadata, key, fn):
    if key in metadata and metadata.get(key) is not None:
        validators.append(partial(fn, metadata.get(key)))
    return validators


def _appender(field):
    validators = []
    appender = partial(_append_to, validators, field.metadata)
    return validators, appender


def _get_instances_of(type_, field):
    if field._default is None:
        return (type_, NONETYPE)
    return type_


@type_dispatch()
def validate(type_, field):
    return []


@validate.register(str)
def _apply_str(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["string"].items():
        validators = appender(k, v)
    validators.append(
        attr.validators.instance_of(_get_instances_of(type_, field))
    )
    return validators


@validate.register(int)
@validate.register(float)
@validate.register(Decimal)
def _apply_number(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["number"].items():
        validators = appender(k, v)
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
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["list"].items():
        validators = appender(k, v)
    validators.append(
        attr.validators.instance_of(_get_instances_of(list, field))
    )
    return validators


@validate.register(typing.Set)
def _validate_set(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["list"].items():
        validators = appender(k, v)
    validators.append(
        attr.validators.instance_of(_get_instances_of(set, field))
    )
    return validators


@validate.register(typing.Dict)
def _validate_dict(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["dict"].items():
        validators = appender(k, v)
    validators.append(
        attr.validators.instance_of(_get_instances_of(dict, field))
    )
    return validators


@validate.register(typing.Union)
def _validate_union(type_, field):
    validator_types = []
    for arg in type_.__args__:
        if arg == NONETYPE:
            validator_types.append(NONETYPE)
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

    if validator_types:
        return [attr.validators.instance_of(tuple(validator_types))]
    return []
