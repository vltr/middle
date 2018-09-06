import logging
from contextlib import contextmanager
from functools import partial

import attr

logger = logging.getLogger(__name__)


@attr.s(hash=True)
class _Config:
    __params = attr.ib(type=dict, factory=dict)
    __param_types = attr.ib(type=dict, factory=dict)
    __changed_params = attr.ib(type=dict, factory=dict)

    def __attrs_post_init__(self):
        self.add_option("force_str", bool, False)
        self.add_option("str_method", bool, True)
        self.add_option("no_transit_local_dtime", bool, False)

    def __getcfg(self, cfgkey=None):
        if cfgkey is None:  # noqa
            return
        if cfgkey in self.__changed_params:  # noqa
            return self.__changed_params.get(cfgkey)
        return self.__params.get(cfgkey)

    def __setcfg(self, value, cfgkey=None, type_=None):
        if cfgkey is None or type_ is None:  # noqa
            return
        if isinstance(value, type_):
            self.__params[cfgkey] = value

    def add_option(self, cfgkey, type_, default):
        setattr(
            self.__class__,
            cfgkey,
            property(
                partial(self.__class__.__getcfg, cfgkey=cfgkey),
                partial(self.__class__.__setcfg, cfgkey=cfgkey, type_=type_),
            ),
        )
        self.__setcfg(default, cfgkey, type_)
        self.__param_types[cfgkey] = type_

    @contextmanager
    def temp(self, **kwargs):
        if kwargs:
            for p in self.__params:
                if p in kwargs:
                    if isinstance(kwargs.get(p), self.__param_types.get(p)):
                        self.__changed_params.update({p: kwargs.get(p)})
                    else:
                        logger.warning(
                            'The config value provided for "{}" doesn\'t match type {!r}'.format(
                                p, self.__param_types.get(p)
                            )
                        )

        yield
        self.__changed_params.clear()


config = _Config()


__all__ = "config"

# there is no much proud in this class, but it will have its purposes
