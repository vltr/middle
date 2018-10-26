import typing
from decimal import Decimal

import attr

from ..exceptions import ValidationError
from .base_validator import BaseValidator


@attr.s(slots=True, hash=True)
class NumberValidator(BaseValidator):
    minimum = attr.ib(type=typing.Union[int, float], default=None)
    maximum = attr.ib(type=typing.Union[int, float], default=None)
    exclusive_minimum = attr.ib(type=bool, default=False)
    exclusive_maximum = attr.ib(type=bool, default=False)
    multiple_of = attr.ib(type=typing.Union[int, float], default=None)

    def __call__(self, inst, attr, value):
        if attr.default is None and value is None:
            return
        minimum = self.minimum
        maximum = self.maximum
        multiple_of = self.multiple_of

        if minimum is not None:
            if self.exclusive_minimum:
                if value <= minimum:
                    raise ValidationError(
                        "'{}' must have a (exclusive) minimum value of {}".format(
                            attr.name, minimum
                        )
                    )
            else:
                if value < minimum:
                    raise ValidationError(
                        "'{}' must have a minimum value of {}".format(
                            attr.name, minimum
                        )
                    )
        if maximum is not None:
            if self.exclusive_maximum:
                if value >= maximum:
                    raise ValidationError(
                        "'{}' must have a (exclusive) maximum value of {}".format(
                            attr.name, maximum
                        )
                    )
            else:
                if value > maximum:
                    raise ValidationError(
                        "'{}' must have a maximum value of {}".format(
                            attr.name, maximum
                        )
                    )
        if multiple_of is not None:
            is_multiple_of = True
            if (
                isinstance(multiple_of, float)
                and float(Decimal(str(value)) % Decimal(str(multiple_of)))
                != 0.0
            ):
                is_multiple_of = False
            if isinstance(multiple_of, int) and value % multiple_of != 0:
                is_multiple_of = False
            if not is_multiple_of:
                raise ValidationError(
                    "'{}' must be multiple of {}".format(
                        attr.name, multiple_of
                    )
                )
