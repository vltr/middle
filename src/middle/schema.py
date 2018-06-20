from functools import partial
from functools import singledispatch

import attr

from .converters import converter
from .converters import model_converter
from .options import metadata_aliases
from .validators import max_str_len
from .validators import min_max_str_len
from .validators import min_str_len
from .validators import str_pattern


def field(*args, **kwargs):
    for alias_group in metadata_aliases.values():
        for alias in alias_group:
            value = kwargs.pop(alias, None)
            if value is not None:
                if kwargs.get("metadata", None) is None:
                    kwargs.update({"metadata": {alias: value}})
                else:
                    kwargs["metadata"].update({alias: value})
    return attr.ib(*args, **kwargs)


class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        if bases:
            for k, f in attrs.items():
                annotations = attrs.get("__annotations__", {})
                _implement_converter(f, k, annotations)
                _implement_validators(f, k, annotations)
        return attr.s(super().__new__(mcls, name, bases, attrs))

    def __call__(cls, *args, **kwargs):
        if args:
            for arg in args:
                if arg is None or isinstance(arg, (bool, int, float, list)):
                    raise TypeError("better error handling")  # TODO
                elif isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    kwargs.update(
                        {
                            f.name: getattr(arg, f.name)
                            for f in attr.fields(cls)
                        }
                    )
        return super().__call__(**kwargs)


# --------------------------------------------------------------- #
# Converters
# --------------------------------------------------------------- #


@converter.register(ModelMeta)  # to avoid circular dependency
def _converter_model_meta(type_):
    return partial(model_converter, type_)


def _implement_converter(field, key, annotations):
    converter_fn = None

    if hasattr(field, "type") and field.type:
        converter_fn = converter(field.type)
    elif key in annotations:
        converter_fn = converter(annotations.get(key))

    if converter_fn is not None:
        field.converter = attr.converters.optional(converter_fn)


# --------------------------------------------------------------- #
# Validators
# --------------------------------------------------------------- #


def _implement_validators(field, key, annotations):
    if hasattr(field, "type") and field.type:
        _implement_validator(field.type, field)
    elif key in annotations:
        _implement_validator(annotations.get(key), field)


@singledispatch
def _implement_validator(type_, field):
    if type_ == str:
        validator = None
        if (
            "min_length" in field.metadata
            and "max_length" not in field.metadata
        ):
            validator = min_str_len
        elif (
            "max_length" in field.metadata
            and "min_length" not in field.metadata
        ):
            validator = max_str_len
        elif "min_length" in field.metadata and "max_length" in field.metadata:
            validator = min_max_str_len

        if "pattern" in field.metadata:
            validator = str_pattern

        if validator is not None:
            field.validator(validator)
        # TODO implement format
    # TODO number (minimum, maximum, exclusive_minimum, exclusive_maximum, multiple_of)
    # TODO array (one_of, min_items, max_items, unique_items)
    # TODO object (min_properties, max_properties)


class Model(metaclass=ModelMeta):
    pass
