import re
from functools import partial

import attr

_sentinel = object()
_type_messages = {
    int: "an integer",
    str: "a string",
    (int, float): "a number",
    bool: "a bool",
    "regex": "either a string representing a regular expression or a regular "
    "expression object",
}


def _is_of_type(value, type_=int):
    if isinstance(value, type_):
        return value
    return _sentinel


def _is_regex(value):
    if isinstance(value, str):
        return re.compile(value)
    elif hasattr(value, "match"):
        return value
    return _sentinel


@attr.s
class MetadataOption:
    name = attr.ib()
    type_ = attr.ib(default=int)
    metadata_chk = attr.ib(default=None)
    accept_lt_zero = attr.ib(default=True)
    upper_range = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.metadata_chk is None:
            self.metadata_chk = partial(_is_of_type, type_=self.type_)

    def __call__(self, value, alias=None):
        value = self.metadata_chk(value)
        if value == _sentinel:
            raise TypeError(
                "The '{}' keyword must be {}".format(
                    alias or self.name, _type_messages.get(self.type_)
                )
            )
        if (
            self.type_ in [int, float, (int, float)]
            and self.accept_lt_zero is False
        ):
            if value < 0:
                raise ValueError(
                    "The '{}' keyword must not be lower than zero".format(
                        alias or self.name
                    )
                )
        return value

    def check_upper_range(self, upper_value, lower_value=None):
        upper_value = self(upper_value, self.upper_range)
        if lower_value is not None and lower_value >= upper_value:
            raise ValueError(
                "The '{}' keyword value must not be equal or greater than the "
                "'{}' keyword value.".format(self.name, self.upper_range)
            )
        return upper_value

    @property
    def keys(self):
        res = [self.name]
        if self.upper_range is not None:
            res.append(self.upper_range)
        return res


metadata_options = [
    MetadataOption(name="description", type_=str),
    MetadataOption(name="minimum", upper_range="maximum", type_=(int, float)),
    MetadataOption(name="exclusive_minimum", type_=bool),
    MetadataOption(name="exclusive_maximum", type_=bool),
    MetadataOption(
        name="multiple_of", type_=(int, float), accept_lt_zero=False
    ),
    MetadataOption(
        name="min_length", upper_range="max_length", accept_lt_zero=False
    ),
    MetadataOption(name="format", type_=str),
    MetadataOption(name="pattern", type_="regex", metadata_chk=_is_regex),
    MetadataOption(
        name="min_items", upper_range="max_items", accept_lt_zero=False
    ),
    MetadataOption(name="unique_items", type_=bool),
    MetadataOption(
        name="min_properties",
        upper_range="max_properties",
        accept_lt_zero=False,
    ),
]

__all__ = ("metadata_options", "MetadataOption")
