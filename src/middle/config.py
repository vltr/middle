import logging
from contextlib import contextmanager
from functools import partial

import attr

logger = logging.getLogger(__name__)


@attr.s(repr=False, slots=True, hash=True)
class _Config:
    _force_str: bool = attr.ib(default=False)
    _str_method: bool = attr.ib(default=True)
    _force_datetime_utc: bool = attr.ib(default=False)
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
    force_datetime_utc = property(
        partial(__getcfg, cfgkey="force_datetime_utc"),
        partial(__setcfg, cfgkey="force_datetime_utc", type_=bool),
    )

    @contextmanager
    def temp(self, **kwargs):
        if kwargs:
            for field in attr.fields(self.__class__):
                field_name = field.name.lstrip("_")
                if field_name in kwargs:
                    if isinstance(kwargs.get(field_name), field.type):
                        self.__changed_params.update(
                            {field_name: kwargs.get(field_name)}
                        )
                    else:
                        logger.warn(
                            'The config value provided for "{}" doesn\'t match type {!r}'.format(
                                field_name, field.type
                            )
                        )
        yield
        self.__changed_params.clear()


config = _Config()


__all__ = "config"
