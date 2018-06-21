import re
from functools import partial
from functools import singledispatch

import attr
from attr._make import _CountingAttr  # NOTE: this is internal to attrs

from .converters import converter
from .converters import model_converter
from .options import metadata_aliases
from .validators import max_num_value
from .validators import max_str_len
from .validators import min_num_value
from .validators import min_str_len
from .validators import num_multiple_of
from .validators import str_pattern

_reserved_keys = re.compile("^__[a-z0-9_]+__$", re.I)
_attr_s_kwargs = {"cmp": False}


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
            annotations = attrs.get("__annotations__", {})
            for k, v in annotations.items():
                if _reserved_keys.match(k):
                    continue
                if k not in attrs:
                    attrs.update(
                        {k: _translate_to_attrib(k, None, annotations, name)}
                    )
            for k, f in attrs.items():
                if _reserved_keys.match(k):
                    continue
                if not isinstance(f, _CountingAttr):
                    f, type_ = _translate_to_attrib(k, f, annotations, name)
                    attrs[k] = f
                    annotations.update({k: type_})
                _implement_converter(f, k, annotations)
                _implement_validators(f, k, annotations)
            if "__annotations__" not in attrs:
                attrs["__annotations__"] = annotations
            else:
                for k in annotations:
                    if k not in attrs["__annotations__"]:
                        attrs["__annotations__"].update({k: annotations[k]})
        attr_kwargs = _attr_s_kwargs.copy()
        if attrs.get("__attr_s_kwargs__", None) is not None:
            attr_kwargs = attrs.get("__attr_s_kwargs__")
            if "init" in attr_kwargs:
                attr_kwargs.pop("init")
        return attr.s(**attr_kwargs)(super().__new__(mcls, name, bases, attrs))

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


class Model(metaclass=ModelMeta):
    pass


# --------------------------------------------------------------- #
# Simple member definition to attr.ib
# --------------------------------------------------------------- #


def _translate_to_attrib(key, data, annotations, cls_name):
    if not isinstance(data, dict):
        data = {}
    type_ = data.pop("type", annotations.get(key, None))
    if type_ is None:
        raise TypeError(
            "type not specified for field {}.{}".format(cls_name, key)
        )
    return field(**data), type_


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
    validators = []
    if type_ == str:
        if "min_length" in field.metadata:
            validators.append(min_str_len)
        if "max_length" in field.metadata:
            validators.append(max_str_len)
        if "pattern" in field.metadata:
            validators.append(str_pattern)

        # TODO implement format
    elif type_ in (int, float):
        if "minimum" in field.metadata:
            validators.append(min_num_value)
        if "maximum" in field.metadata:
            validators.append(max_num_value)
        if "multiple_of" in field.metadata:
            validators.append(num_multiple_of)

    # TODO array (one_of, min_items, max_items, unique_items)
    # TODO object (min_properties, max_properties)

    if len(validators):
        for validator in validators:
            field.validator(validator)
