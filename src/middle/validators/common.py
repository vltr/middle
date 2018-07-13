import re
from decimal import Decimal

from ..exceptions import ValidationError

_sentinel = object()
_type_messages = {
    int: "an integer",
    str: "a string",
    (int, float): "a number",
    bool: "a bool",
}


def _check_meta_value(meta_value, types, kwarg, deny_negative=True):
    if not isinstance(meta_value, types):
        raise TypeError(
            "The '{}' keyword must be {}".format(
                kwarg, _type_messages.get(types)
            )
        )
    if (
        deny_negative
        and isinstance(meta_value, (int, float))
        and meta_value < 0
    ):
        raise ValueError("The '{}' keyword must not be negative".format(kwarg))


def _check_max_counterpart(meta_value, attribute, kwarg, max_kwarg):
    max_counterpart = attribute.metadata.get(max_kwarg, _sentinel)
    if max_counterpart == _sentinel:
        return
    if meta_value >= max_counterpart:
        raise ValueError(
            "The '{}' keyword value must not be equal or greater than the "
            "'{}' keyword value.".format(kwarg, max_kwarg)
        )


def _in_case_of_none(func):
    def wrapper(meta_value, instance, attribute, value):
        if meta_value is None or (attribute.default is None and value is None):
            return
        return func(meta_value, instance, attribute, value)

    return wrapper


@_in_case_of_none
def min_str_len(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, int, "min_length")
    _check_max_counterpart(meta_value, attribute, "min_length", "max_length")
    if len(value) < meta_value:
        raise ValidationError(
            "'{}' must have a minimum length of {} chars".format(
                attribute.name, meta_value
            )
        )


@_in_case_of_none
def max_str_len(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, int, "max_length")
    if len(value) > meta_value:
        raise ValidationError(
            "'{}' must have a maximum length of {} chars".format(
                attribute.name, meta_value
            )
        )


@_in_case_of_none
def str_pattern(meta_value, instance, attribute, value):
    if isinstance(meta_value, str):
        match = re.match(meta_value, value)
    elif hasattr(meta_value, "match"):
        match = meta_value.match(value)
    else:
        raise TypeError(
            "The pattern attribute must be either a string "
            "representing a regular expression or a regular "
            "expression object"
        )
    if match is None:
        raise ValidationError(
            "'{}' did not match the given pattern: '{}'".format(
                attribute.name, meta_value
            )
        )


@_in_case_of_none
def min_num_value(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, (int, float), "minimum", False)
    _check_max_counterpart(meta_value, attribute, "minimum", "maximum")
    exclusive_min = attribute.metadata.get("exclusive_minimum", False)
    _check_meta_value(exclusive_min, bool, "exclusive_minimum")
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


@_in_case_of_none
def max_num_value(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, (int, float), "maximum", False)
    exclusive_max = attribute.metadata.get("exclusive_maximum", False)
    _check_meta_value(exclusive_max, bool, "exclusive_maximum")
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


@_in_case_of_none
def num_multiple_of(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, (int, float), "multiple_of")
    is_multiple_of = True
    if (
        isinstance(meta_value, float)
        and float(Decimal(str(value)) % Decimal(str(meta_value))) != 0.
    ):
        is_multiple_of = False
    if isinstance(meta_value, int) and value % meta_value != 0:
        is_multiple_of = False
    if not is_multiple_of:
        raise ValidationError(
            "'{}' must be multiple of {}".format(attribute.name, meta_value)
        )


@_in_case_of_none
def list_min_items(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, int, "min_items")
    _check_max_counterpart(meta_value, attribute, "min_items", "max_items")
    if len(value) < meta_value:
        raise ValidationError(
            "'{}' has no enough items of {}".format(attribute.name, meta_value)
        )


@_in_case_of_none
def list_max_items(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, int, "max_items")
    if len(value) > meta_value:
        raise ValidationError(
            "'{}' has more items than the limit of {}".format(
                attribute.name, meta_value
            )
        )


@_in_case_of_none
def list_unique_items(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, bool, "unique_items")
    if meta_value:
        if isinstance(value, set):
            value = list(value)
        for v in value:
            if value.count(v) > 1:
                raise ValidationError(
                    "'{}' must only have unique items".format(attribute.name)
                )


@_in_case_of_none
def dict_min_properties(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, int, "min_properties")
    _check_max_counterpart(
        meta_value, attribute, "min_properties", "max_properties"
    )
    if len(value.keys()) < meta_value:
        raise ValidationError(
            "'{}' has no enough properties of {}".format(
                attribute.name, meta_value
            )
        )


@_in_case_of_none
def dict_max_properties(meta_value, instance, attribute, value):
    _check_meta_value(meta_value, int, "max_properties")
    if len(value.keys()) > meta_value:
        raise ValidationError(
            "'{}' has more properties than the limit of {}".format(
                attribute.name, meta_value
            )
        )


FOR_TYPE = {
    "string": {
        "min_length": min_str_len,
        "max_length": max_str_len,
        "pattern": str_pattern,
        # {"format": ...},  # TODO
    },
    "number": {
        "minimum": min_num_value,
        "maximum": max_num_value,
        "multiple_of": num_multiple_of,
    },
    "list": {
        "min_items": list_min_items,
        "max_items": list_max_items,
        "unique_items": list_unique_items,
        # {"one_of": ...},  # TODO
    },
    "dict": {
        "min_properties": dict_min_properties,
        "max_properties": dict_max_properties,
    },
}

# UNSOLVED BUSINESS BELLOW :-)
#
# def _remove_nones(meta_values):
#     return {k: v for k, v in meta_values.items() if v is not None}


# def _check_meta_values(meta_values, types, deny_negative=True):
#     for k, v in meta_values:
#         if not isinstance(v, types):
#             raise TypeError(
#                 "The '{}' keyword must be {}".format(
#                     k, _type_messages.get(types)
#                 )
#             )
#         if deny_negative:
#             raise TypeError("The '{}' keyword must not be negative".format(k))


# def _in_case_of_none(func):
#     def wrapper(meta_value, instance, attribute, value):
#         if meta_value is None or (attribute.default is None and value is None):
#             return
#         return func(meta_value, instance, attribute, value)

#     return wrapper


# @_in_case_of_none
# def min_max_str_len(meta_values, instance, attribute, value):
#     mv = _remove_nones(meta_values)
#     _check_meta_values(mv, int)
#     _check_max_counterpart(meta_value, attribute, "min_length", "max_length")
#     if len(value) < meta_value:
#         raise ValidationError(
#             "'{}' must have a minimum length of {} chars".format(
#                 attribute.name, meta_value
#             )
#         )
