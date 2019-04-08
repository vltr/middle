import attr

from ..ast import build_dict_validator
from .base_validator import BaseValidator


@attr.s(slots=True, hash=True)
class DictValidator(BaseValidator):
    min_properties = attr.ib(type=int, default=None)
    max_properties = attr.ib(type=int, default=None)

    def __attrs_post_init__(self):
        self._validate = build_dict_validator(
            min_properties=self.min_properties,
            max_properties=self.max_properties,
        )

    def __call__(self, inst, attr, value):
        self._validate(attr, value)
