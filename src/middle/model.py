import re
from functools import partial

import attr
from attr._make import _CountingAttr  # NOTE: this is internal to attrs

from .compat import TYPE_REGISTRY
from .converters import converter
from .converters import model_converter
from .options import metadata_options
from .utils import asdict
from .utils import value_of
from .validators import validate

_reserved_keys = re.compile("^__[a-z0-9_]+__$", re.I)
_attr_s_kwargs = {"cmp": False}


def field(*args, **kwargs):
    for alias in metadata_options:
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
            for k in annotations.keys():
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
                _implement_converters(f, k, annotations)
                _implement_validators(f, k, annotations)
            if "__annotations__" not in attrs:
                attrs["__annotations__"] = annotations
            else:
                for k in annotations:
                    if k not in attrs["__annotations__"]:
                        # XXX does it get here?
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
                if arg is None or isinstance(
                    arg, (str, bool, int, float, list)
                ):  # no str, ``middle`` won't parse a thing
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
# Add the Model class itself to TYPE_REGISTRY
# --------------------------------------------------------------- #

TYPE_REGISTRY[ModelMeta] = Model

# --------------------------------------------------------------- #
# Simple member definition to attr.ib
# --------------------------------------------------------------- #


def _translate_to_attrib(key, data, annotations, cls_name):
    if not isinstance(data, dict):
        data = {}
    anchor = object()
    type_ = data.pop("type", annotations.get(key, anchor))
    if type_ == anchor:
        raise TypeError(
            "type not specified for field {}.{}".format(cls_name, key)
        )
    return field(**data), type_


# --------------------------------------------------------------- #
# Util
# --------------------------------------------------------------- #


@value_of.register(Model)  # to avoid circular dependency
@value_of.register(ModelMeta)
def _value_of_model(type_):
    return asdict


# --------------------------------------------------------------- #
# Converters
# --------------------------------------------------------------- #


@converter.register(Model)  # to avoid circular dependency
@converter.register(ModelMeta)  # to avoid circular dependency
def _converter_model_meta(type_):
    return partial(model_converter, type_)


def _implement_converters(field, key, annotations):
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


@validate.register(Model)  # to avoid circular dependency
@validate.register(ModelMeta)  # to avoid circular dependency
def _validate_model_meta(type_, field):
    return [attr.validators.instance_of(Model)]


def _implement_validators(field, key, annotations):
    if hasattr(field, "type") and field.type:
        for v in validate(field.type, field):
            field.validator(v)
    elif key in annotations:
        for v in validate(annotations.get(key), field):
            field.validator(v)
