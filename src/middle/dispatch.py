from functools import lru_cache

import attr

from .compat import get_type


@attr.s(cmp=False, slots=True)
class _TypeDispatch:
    _default_fn = attr.ib()
    _name = attr.ib(init=False)
    _registry = attr.ib(init=False)
    _get_fn_cache = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._name = self._default_fn.__name__
        self._registry = {}
        self._get_fn_cache = lru_cache(maxsize=None)(self._get_fn)

    def _get_fn(self, type_):
        return self._registry.get(get_type(type_), self._default_fn)

    def __call__(self, *args):
        fn = self._get_fn_cache(args[0])
        return fn(*args)

    def register(self, type_, fn=None):
        if fn is None:
            return lambda f: self.register(type_, f)
        if type_ in self._registry:
            raise TypeError(
                "Type '{!r}' is already registered for function '{}'".format(
                    type_, self._name
                )
            )
        self._registry[type_] = fn
        return fn

    def unregister(self, type_):
        if type_ in self._registry:
            del self._registry[type_]
            self._get_fn_cache.cache_clear()


def type_dispatch(lru=False):
    def inner(fn):
        td = _TypeDispatch(default_fn=fn)
        if lru:
            lru_td = lru_cache(maxsize=2048)(td)
            lru_td.register = td.register
            lru_td.unregister = td.unregister
            return lru_td
        return td

    return inner


__all__ = "type_dispatch"
