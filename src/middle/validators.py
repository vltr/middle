import re


class ValidationError(Exception):
    pass


def min_str_len(instance, attribute, value):
    min_length = attribute.metadata.get("min_length", None)
    if min_length is None:
        return
    if len(value) <= min_length:
        raise ValidationError(
            "'{}' must have a minimum length of {} chars".format(
                attribute.name, min_length
            )
        )


def max_str_len(instance, attribute, value):
    max_length = attribute.metadata.get("max_length", None)
    if max_length is None:
        return
    if len(value) > max_length:
        raise ValidationError(
            "'{}' must have a maximum length of {} chars".format(
                attribute.name, max_length
            )
        )


def str_pattern(instance, attribute, value):
    pattern = attribute.metadata.get("pattern", None)
    if pattern is None:
        return
    if re.match(pattern, value) is None:
        raise ValidationError(
            "'{}' did not match the given pattern: '{}'".format(
                attribute.name, pattern
            )
        )


def min_num_value(instance, attribute, value):
    min_value = attribute.metadata.get("minimum", None)
    exclusive_min = attribute.metadata.get("exclusive_minimum", False)
    if min_value is None:
        return
    if exclusive_min:
        if value <= min_value:
            raise ValidationError(
                "'{}' must have a (exclusive) minimum value of {}".format(
                    attribute.name, min_value
                )
            )
    else:
        if value < min_value:
            raise ValidationError(
                "'{}' must have a minimum value of {}".format(
                    attribute.name, min_value
                )
            )


def max_num_value(instance, attribute, value):
    max_value = attribute.metadata.get("maximum", None)
    exclusive_max = attribute.metadata.get("exclusive_maximum", False)
    if max_value is None:
        return
    if exclusive_max:
        if value >= max_value:
            raise ValidationError(
                "'{}' must have a (exclusive) maximum value of {}".format(
                    attribute.name, max_value
                )
            )
    else:
        if value > max_value:
            raise ValidationError(
                "'{}' must have a maximum value of {}".format(
                    attribute.name, max_value
                )
            )


def num_multiple_of(instance, attribute, value):
    multiple_of = attribute.metadata.get("multiple_of", None)
    if multiple_of is None:
        return
    if value % multiple_of != 0:
        raise ValidationError(
            "'{}' must be multiple of {}".format(attribute.name, multiple_of)
        )


# def arr_min_length(instance, attribute, value):
#     min_items = attribute.metadata.get("min_items", None)
#     if min_items is None:
#         return
