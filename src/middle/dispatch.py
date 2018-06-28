from functools import update_wrapper
from types import MappingProxyType

from .compat import get_type


def type_dispatch(func):
    """A simpler version of Python's singledispatch own implementation
    """

    registry = {}

    def dispatch(cls):
        cls = get_type(cls)
        try:
            impl = registry[cls]
        except KeyError:
            impl = registry[object]
        return impl

    def register(cls, func=None):
        if func is None:
            return lambda f: register(cls, f)
        registry[cls] = func
        return func

    def wrapper(*args, **kw):
        return dispatch(args[0])(*args, **kw)

    def unregister(cls):
        if cls in registry:
            del registry[cls]

    registry[object] = func
    wrapper.register = register
    wrapper.unregister = unregister
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    update_wrapper(wrapper, func)
    return wrapper


__all__ = "type_dispatch"
