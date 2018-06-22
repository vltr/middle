import re
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
from .exceptions import ValidationError


def min_str_len(meta_value, instance, attribute, value):
    if len(value) <= meta_value:
        raise ValidationError(
            "'{}' must have a minimum length of {} chars".format(
                attribute.name, meta_value
            )
        )


def max_str_len(meta_value, instance, attribute, value):
    if len(value) > meta_value:
        raise ValidationError(
            "'{}' must have a maximum length of {} chars".format(
                attribute.name, meta_value
            )
        )


def str_pattern(meta_value, instance, attribute, value):
    if re.match(meta_value, value) is None:
        raise ValidationError(
            "'{}' did not match the given pattern: '{}'".format(
                attribute.name, meta_value
            )
        )


def min_num_value(meta_value, instance, attribute, value):
    exclusive_min = attribute.metadata.get("exclusive_minimum", False)
    if exclusive_min:
        if value <= meta_value:
            raise ValidationError(
                "'{}' must have a (exclusive) minimum value of {}".format(
                    attribute.name, meta_value
                )
            )
    else:
        if value < meta_value:
            raise ValidationError(
                "'{}' must have a minimum value of {}".format(
                    attribute.name, meta_value
                )
            )


def max_num_value(meta_value, instance, attribute, value):
    exclusive_max = attribute.metadata.get("exclusive_maximum", False)
    if exclusive_max:
        if value >= meta_value:
            raise ValidationError(
                "'{}' must have a (exclusive) maximum value of {}".format(
                    attribute.name, meta_value
                )
            )
    else:
        if value > meta_value:
            raise ValidationError(
                "'{}' must have a maximum value of {}".format(
                    attribute.name, meta_value
                )
            )


def num_multiple_of(meta_value, instance, attribute, value):
    is_multiple_of = True
    if (
        isinstance(meta_value, float)
        and not (value * (1. / meta_value)).is_integer()
    ):
        is_multiple_of = False
    if value % meta_value != 0:
        is_multiple_of = False
    if not is_multiple_of:
        raise ValidationError(
            "'{}' must be multiple of {}".format(attribute.name, meta_value)
        )


def list_min_items(meta_value, instance, attribute, value):
    if len(value) < meta_value:
        raise ValidationError(
            "'{}' has no enough items of {}".format(attribute.name, meta_value)
        )


def list_max_items(meta_value, instance, attribute, value):
    if len(value) > meta_value:
        raise ValidationError(
            "'{}' has more items than the limit of {}".format(
                attribute.name, meta_value
            )
        )


def list_unique_items(meta_value, instance, attribute, value):
    if meta_value:
        for v in value:
            if value.count(v) > 1:
                raise ValidationError(
                    "'{}' must only have unique items".format(attribute.name)
                )


def dict_min_properties(meta_value, instance, attribute, value):
    if len(value.keys()) < meta_value:
        raise ValidationError(
            "'{}' has no enough properties of {}".format(
                attribute.name, meta_value
            )
        )


def dict_max_properties(meta_value, instance, attribute, value):
    if len(value.keys()) > meta_value:
        raise ValidationError(
            "'{}' has more properties than the limit of {}".format(
                attribute.name, meta_value
            )
        )


def _append_to(arr, dct, key, fn):
    if key in dct and dct.get(key) is not None:
        arr.append(partial(fn, dct.get(key)))
    return arr


@singledispatch
def validators(type_, field):
    validators = []
    appender = partial(_append_to, validators, field.metadata)
    if type_ == str:
        validators = appender("min_length", min_str_len)
        validators = appender("max_length", max_str_len)
        validators = appender("pattern", str_pattern)
        # TODO implement format
    elif type_ in (int, float):
        validators = appender("minimum", min_num_value)
        validators = appender("maximum", max_num_value)
        validators = appender("multiple_of", num_multiple_of)
    elif attr.has(type_):
        pass

    return validators


if IS_PY37:

    @validators.register(GenericType)
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
            # TODO array (one_of, min_items, max_items, unique_items)
            # validators = appender("one_of", )
            validators = appender("min_items", list_min_items)
            validators = appender("max_items", list_max_items)
            validators = appender("unique_items", list_unique_items)
        elif type_._name in ("Dict", "Mapping", "MutableMapping"):
            # TODO object (min_properties, max_properties)
            validators = appender("min_properties", dict_min_properties)
            validators = appender("max_properties", dict_max_properties)
        else:
            print("converters.py")
            # from IPython import embed

            # embed()
            raise TypeError("This type is not supported")  # TODO


else:

    @validators.register(GenericType)
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
            # TODO array (one_of, min_items, max_items, unique_items)
            # validators = appender("one_of", )
            validators = appender("min_items", list_min_items)
            validators = appender("max_items", list_max_items)
            validators = appender("unique_items", list_unique_items)
        elif type_.__base__ in (Dict, Mapping, MutableMapping):
            # TODO object (min_properties, max_properties)
            validators = appender("min_properties", dict_min_properties)
            validators = appender("max_properties", dict_max_properties)
        else:
            print("converters.py")
            # from IPython import embed

            # embed()
            raise TypeError("This type is not supported")  # TODO
        return validators
