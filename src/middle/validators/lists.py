import attr

from ..exceptions import ValidationError
from .base_validator import BaseValidator


@attr.s(slots=True, hash=True)
class ListValidator(BaseValidator):
    min_items = attr.ib(type=int, default=None)
    max_items = attr.ib(type=int, default=None)
    unique_items = attr.ib(type=bool, default=False)
    # one_of = attr.ib()  # TODO

    def __call__(self, inst, attr, value):
        if attr.default is None and value is None:
            return

        min_items = self.min_items
        max_items = self.max_items
        unique_items = self.unique_items

        total_size = len(value)

        if min_items is not None:
            if total_size < min_items:
                raise ValidationError(
                    "'{}' has no enough items of {}".format(
                        attr.name, min_items
                    )
                )
        if max_items is not None:
            if total_size > max_items:
                raise ValidationError(
                    "'{}' has more items than the limit of {}".format(
                        attr.name, max_items
                    )
                )
        if unique_items and isinstance(value, list):
            for v in value:
                if value.count(v) > 1:
                    raise ValidationError(
                        "'{}' must only have unique items".format(attr.name)
                    )
