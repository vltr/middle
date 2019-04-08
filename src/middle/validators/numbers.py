import typing

import attr

from ..ast import build_number_validator
from .base_validator import BaseValidator


@attr.s(slots=True, hash=True)
class NumberValidator(BaseValidator):
    minimum = attr.ib(type=typing.Union[int, float], default=None)
    maximum = attr.ib(type=typing.Union[int, float], default=None)
    exclusive_minimum = attr.ib(type=bool, default=False)
    exclusive_maximum = attr.ib(type=bool, default=False)
    multiple_of = attr.ib(type=typing.Union[int, float], default=None)

    def __attrs_post_init__(self):
        self._validate = build_number_validator(
            minimum=self.minimum,
            maximum=self.maximum,
            multiple_of=self.multiple_of,
            exclusive_minimum=self.exclusive_minimum,
            exclusive_maximum=self.exclusive_maximum,
        )

    def __call__(self, inst, attr, value):
        self._validate(attr, value)
