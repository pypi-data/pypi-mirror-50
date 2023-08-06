# coding=utf-8

import logging

from .utils import load_object
from . import events
from .errors import NotEnabled

log = logging.getLogger(__name__)


class MiddlewareManager:
    def __init__(self, *middlewares):
        self._open_handlers = []
        self._close_handlers = []
        self.components = []
        for middleware in middlewares:
            self._add_middleware(middleware)

    @classmethod
    def _middleware_list_from_config(cls, config):
        raise NotImplementedError

    @classmethod
    def from_crawler(cls, crawler):
        mw_list = cls._middleware_list_from_config(crawler.config)
        mws = []
        for cls_path in mw_list:
            mw_cls = load_object(cls_path)
            try:
                if hasattr(mw_cls, "from_crawler"):
                    mw = mw_cls.from_crawler(crawler)
                else:
                    mw = mw_cls()
            except NotEnabled:
                log.debug('%s is not enabled', cls_path)
            else:
                mws.append(mw)
        mwm = cls(*mws)
        crawler.event_bus.subscribe(mwm.open, events.crawler_start)
        crawler.event_bus.subscribe(mwm.close, events.crawler_shutdown)
        return mwm

    def _add_middleware(self, middleware):
        self.components.append(middleware)
        if hasattr(middleware, "open"):
            self._open_handlers.append(middleware.open)
        if hasattr(middleware, "close"):
            self._close_handlers.insert(0, middleware.close)

    @staticmethod
    def _priority_list_from_config(name, config):
        c = config.get(name)
        assert c is None or isinstance(c, (list, dict)), \
            "'{}' must be None, a list or a dict, got {}".format(name, type(c).__name__)
        if c is None:
            return {}
        d = {}
        if isinstance(c, dict):
            for i in c:
                d[i] = (float(c[i]),)
        elif isinstance(c, list):
            for i in range(len(c)):
                d[c[i]] = (0, i)
        return d

    @classmethod
    def _make_component_list(cls, name, config):
        c_base = cls._priority_list_from_config('default_' + name, config)
        c = cls._priority_list_from_config(name, config)
        c_base.update(c)
        res = []
        for k, v in c_base.items():
            if v is not None:
                res.append((k, v))
        res.sort(key=lambda x: x[1])
        return [i[0] for i in res]

    def open(self):
        for method in self._open_handlers:
            method()

    def close(self):
        for method in self._close_handlers:
            method()
