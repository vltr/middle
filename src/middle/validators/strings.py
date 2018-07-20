import re
import typing

import attr

from ..compat import RegexPatternType
from ..exceptions import ValidationError
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

    def __call__(self, inst, attr, value):
        if attr.default is None and value is None:
            return

        min_length = self.min_length
        max_length = self.max_length
        pattern = self._re_instance

        if min_length is not None:
            if len(value) < min_length:
                raise ValidationError(
                    "'{}' must have a minimum length of {} chars".format(
                        attr.name, min_length
                    )
                )
        if max_length is not None:
            if len(value) > max_length:
                raise ValidationError(
                    "'{}' must have a maximum length of {} chars".format(
                        attr.name, max_length
                    )
                )
        if pattern is not None:
            match = pattern.match(value)
            if match is None:
                raise ValidationError(
                    "'{}' did not match the given pattern: '{}'".format(
                        attr.name, self.pattern
                    )
                )
