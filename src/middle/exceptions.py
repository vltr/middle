_EXTENDING_URL = "https://middle.readthedocs.io/en/latest/extending.html"


class MiddleException(Exception):  # personal note: weird name ...
    """Base Exception for all ``middle`` errors."""


class ValidationError(MiddleException):
    pass


class InvalidType(MiddleException):
    def __init__(self, message=None, *args, **kwargs):
        if message is None:
            message = (
                "The required type is not supported by ``middle``. "
                "Please, see {} for more information on how to add "
                "your own types.".format(_EXTENDING_URL)
            )
        super().__init__(message)


__all__ = ("MiddleException", "ValidationError", "InvalidType")
