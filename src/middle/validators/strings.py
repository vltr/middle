import re
import typing

import attr

from ..ast import build_string_validator
from ..compat import RegexPatternType
from .base_validator import BaseValidator


@attr.s(slots=True, hash=True)
class StringValidator(BaseValidator):
    min_length = attr.ib(type=int, default=None)
    max_length = attr.ib(type=int, default=None)
    pattern = attr.ib(type=typing.Union[RegexPatternType, str], default=None)
    _re_instance = attr.ib(type=RegexPatternType, default=None)
    # format = attr.ib(type=str, default=None)  # TODO

    def __attrs_post_init__(self):
        if self.pattern is not None:
            if isinstance(self.pattern, RegexPatternType):
                inst = self.pattern
                self.pattern = inst.pattern
                self._re_instance = inst
            elif isinstance(self.pattern, str):
                self._re_instance = re.compile(self.pattern)
        self._validate = build_string_validator(
            min_length=self.min_length,
            max_length=self.max_length,
            re_instance=self._re_instance,
        )

    def __call__(self, inst, attr, value):
        self._validate(attr, value)
