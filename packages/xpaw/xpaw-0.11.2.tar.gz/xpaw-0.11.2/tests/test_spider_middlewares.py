# coding=utf-8

from xpaw.spider_middlewares import *
from xpaw.http import HttpRequest
from xpaw.item import Item
from .crawler import Crawler


class TestDepthMiddleware:
    def test_handle_output(self):
        class R:
            def __init__(self, depth=None):
                self.meta = {}
                if depth is not None:
                    self.meta['depth'] = depth

        mw = DepthMiddleware.from_crawler(Crawler(max_depth=1))
        req = HttpRequest("http://python.org/", "GET")
        item = Item()
        res = [i for i in mw.handle_output(R(), [req, item])]
        assert res == [req, item] and req.meta['depth'] == 1
        res = [i for i in mw.handle_output(R(0), [req, item])]
        assert res == [req, item] and req.meta['depth'] == 1
        res = [i for i in mw.handle_output(R(1), [req, item])]
        assert res == [item] and req.meta['depth'] == 2

    def test_handle_start_requests(self):
        mw = DepthMiddleware.from_crawler(Crawler())
        req = HttpRequest("http://python.org/", "GET")
        res = [i for i in mw.handle_start_requests([req])]
        for r in res:
            assert r.meta.get('depth') == 0
