#!/usr/lib/env python
# -*- encoding:utf-8 -*-

from lixingtie.web import RequestHandler, route


@route("/index.html")
class Index(RequestHandler):
    def get(self):
        return self.view("index.html")
