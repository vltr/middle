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

from ..compat import IS_PY37
from ..compat import GenericType
from .common import FOR_TYPE

if IS_PY37:
    from typing import Union
else:
    from typing import _Union


def _append_to(arr, dct, key, fn):
    if key in dct and dct.get(key) is not None:
        arr.append(partial(fn, dct.get(key)))
    return arr


@singledispatch
def apply_validators(type_, field):
    validators = []
    appender = partial(_append_to, validators, field.metadata)
    if type_ == str:
        for k, v in FOR_TYPE["string"].items():
            validators = appender(k, v)
        validators.append(attr.validators.instance_of(type_))
    elif type_ in (int, float):
        for k, v in FOR_TYPE["number"].items():
            validators = appender(k, v)
        validators.append(attr.validators.instance_of(type_))
    elif type_ in (bool, date, datetime):
        validators.append(attr.validators.instance_of(type_))
    elif attr.has(type_):
        validators.append(attr.validators.instance_of(type_))
    else:
        print(">> apply_validators @ rules.py")
        from IPython import embed

        embed()

    return validators


@apply_validators.register(EnumMeta)
def _validate_enum(type_, field):
    return [attr.validators.instance_of(type_)]


if IS_PY37:

    @apply_validators.register(GenericType)
    def _validate_generic_meta(type_, field):
        validators = []
        appender = partial(_append_to, validators, field.metadata)
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
            for k, v in FOR_TYPE["list"].items():
                validators = appender(k, v)
            validators.append(attr.validators.instance_of((list, set)))
        elif type_._name in ("Dict", "Mapping", "MutableMapping"):
            for k, v in FOR_TYPE["dict"].items():
                validators = appender(k, v)
            validators.append(attr.validators.instance_of(dict))
        elif hasattr(type_, "__origin__") and type_.__origin__ == Union:
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
                        date,
                        datetime,
                        list,
                        dict,
                    ):
                        validator_types.append(arg)
                    elif attr.has(arg):
                        validator_types.append(arg)

            if validator_types:
                return [attr.validators.instance_of(tuple(validator_types))]
            return []
        else:
            print("validators.py")
            from IPython import embed

            embed()
            raise TypeError("This type is not supported")  # TODO
        return validators


else:

    @apply_validators.register(GenericType)
    def _validate_generic_meta(type_, field):
        validators = []
        appender = partial(_append_to, validators, field.metadata)
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
            for k, v in FOR_TYPE["list"].items():
                validators = appender(k, v)
            validators.append(attr.validators.instance_of((list, set)))
        elif type_.__base__ in (Dict, Mapping, MutableMapping):
            for k, v in FOR_TYPE["dict"].items():
                validators = appender(k, v)
            validators.append(attr.validators.instance_of(dict))
        else:
            print("validators.py")
            from IPython import embed

            embed()
            raise TypeError("This type is not supported")  # TODO
        return validators

    @apply_validators.register(_Union)
    def _validate_union(type_, field):
        ntype = type(None)
        validator_types = []
        for arg in type_.__args__:
            if arg == ntype:
                validator_types.append(ntype)
            else:
                if arg in (str, int, float, bool, date, datetime, list, dict):
                    validator_types.append(arg)
                elif attr.has(arg):
                    validator_types.append(arg)

        if validator_types:
            return [attr.validators.instance_of(tuple(validator_types))]
        return []
