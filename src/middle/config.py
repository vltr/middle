from contextlib import contextmanager
from functools import partial

import attr


@attr.s(repr=False, slots=True, hash=True)
class _Config:
    _force_str: bool = attr.ib(default=False)
    _str_method: bool = attr.ib(default=True)
    __changed_params: dict = attr.ib(default={})

    def __getcfg(self, cfgkey=None):
        if cfgkey is None:  # noqa
            return
        if cfgkey in self.__changed_params:  # noqa
            return self.__changed_params.get(cfgkey)
        return getattr(self, "_{}".format(cfgkey))

    def __setcfg(self, value, cfgkey=None, type_=None):
        if cfgkey is None or type_ is None:  # noqa
            return
        if isinstance(value, type_):
            setattr(self, "_{}".format(cfgkey), value)

    force_str = property(
        partial(__getcfg, cfgkey="force_str"),
        partial(__setcfg, cfgkey="force_str", type_=bool),
    )
    str_method = property(
        partial(__getcfg, cfgkey="str_method"),
        partial(__setcfg, cfgkey="str_method", type_=bool),
    )

    @contextmanager
    def temp(self, **kwargs):
        if kwargs:
            keys = [f.name.lstrip("_") for f in attr.fields(self.__class__)]
            self.__changed_params.update(
                {k: kwargs[k] for k in keys if k in kwargs}
            )
        yield
        self.__changed_params.clear()


config = _Config()


__all__ = "config"
