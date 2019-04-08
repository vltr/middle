import attr

from ..ast import build_list_validator
from .base_validator import BaseValidator


@attr.s(slots=True, hash=True)
class ListValidator(BaseValidator):
    min_items = attr.ib(type=int, default=None)
    max_items = attr.ib(type=int, default=None)
    unique_items = attr.ib(type=bool, default=False)
    # one_of = attr.ib()  # TODO

    def __attrs_post_init__(self):
        self._validate = build_list_validator(
            min_items=self.min_items,
            max_items=self.max_items,
            unique_items=self.unique_items,
        )

    def __call__(self, inst, attr, value):
        self._validate(attr, value)
