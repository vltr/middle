import attr

from ..exceptions import ValidationError
from .base_validator import BaseValidator


@attr.s(slots=True, hash=True)
class DictValidator(BaseValidator):
    min_properties = attr.ib(type=int, default=None)
    max_properties = attr.ib(type=int, default=None)

    def __call__(self, inst, attr, value):
        if attr.default is None and value is None:
            return

        if value is not None:

            min_properties = self.min_properties
            max_properties = self.max_properties

            total_size = len(value.keys())

            if min_properties is not None:
                if total_size < min_properties:
                    raise ValidationError(
                        "'{}' has no enough properties of {}".format(
                            attr.name, min_properties
                        )
                    )
            if max_properties is not None:
                if total_size > max_properties:
                    raise ValidationError(
                        "'{}' has more properties than the limit of {}".format(
                            attr.name, max_properties
                        )
                    )
