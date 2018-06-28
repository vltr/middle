import datetime
import typing
from enum import EnumMeta
from functools import partial

import attr

from ..dispatch import type_dispatch
from .common import FOR_TYPE


def _append_to(arr, dct, key, fn):
    if key in dct and dct.get(key) is not None:
        arr.append(partial(fn, dct.get(key)))
    return arr


def _appender(field):
    validators = []
    appender = partial(_append_to, validators, field.metadata)
    return validators, appender


@type_dispatch
def apply_validators(type_, field):
    return []


@apply_validators.register(str)
def _apply_str(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["string"].items():
        validators = appender(k, v)
    validators.append(attr.validators.instance_of(type_))
    return validators


@apply_validators.register(int)
@apply_validators.register(float)
def _apply_number(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["number"].items():
        validators = appender(k, v)
    validators.append(attr.validators.instance_of(type_))
    return validators


@apply_validators.register(bool)
@apply_validators.register(datetime.date)
@apply_validators.register(datetime.datetime)
def _apply_bool_dt_dttime(type_, field):
    return [attr.validators.instance_of(type_)]


@apply_validators.register(EnumMeta)
def _validate_enum(type_, field):
    return [attr.validators.instance_of(type_)]


@apply_validators.register(typing.List)
@apply_validators.register(typing.Sequence)
@apply_validators.register(typing.Collection)
@apply_validators.register(typing.Iterable)
@apply_validators.register(typing.MutableSequence)
def _validate_list(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["list"].items():
        validators = appender(k, v)
    validators.append(attr.validators.instance_of(list))
    return validators


@apply_validators.register(typing.Set)
@apply_validators.register(typing.MutableSet)
@apply_validators.register(typing.FrozenSet)
def _validate_set(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["list"].items():
        validators = appender(k, v)
    validators.append(attr.validators.instance_of(set))
    return validators


@apply_validators.register(typing.Dict)
@apply_validators.register(typing.Mapping)
@apply_validators.register(typing.MutableMapping)
def _validate_dict(type_, field):
    validators, appender = _appender(field)
    for k, v in FOR_TYPE["dict"].items():
        validators = appender(k, v)
    validators.append(attr.validators.instance_of(dict))
    return validators


@apply_validators.register(typing.Union)
def _validate_union(type_, field):
    ntype = type(None)
    validator_types = []
    for arg in type_.__args__:
        if arg == ntype:
            validator_types.append(ntype)
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
