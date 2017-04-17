#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-8-15

import os
import sys

try:
    from personal import TORNADO_PORT
except:
    try:
        from settings import TORNADO_PORT
    except:
        TORNADO_PORT = 8080

try:
    from settings import LOGIN_URL
except:
    LOGIN_URL = ""

try:
    from settings import COOKIE_SECRET
except:
    COOKIE_SECRET = ""

import os
import tornado.web
import tornado.ioloop
from tornado.options import define, options
from tornado.util import ObjectDict

import framework.mvc.web
import framework.web.url


define("REDIS_HOST", default='localhost', help="redis host", type=str)
define("REDIS_PORT", default=6379, help="redis port", type=int)
define("REDIS_DB", default=0, help="redis db", type=int)


def run(debug=False):
    settings = {
        "debug": debug,
        "static_path": "static",
        "handler_path": "handlers",
        "template_path": "templates",
        "ui_methods": {
            "url": framework.web.url.url,
        }
    }

    if LOGIN_URL:
        settings["login_url"] = LOGIN_URL

    if COOKIE_SECRET:
        settings["cookie_secret"] = COOKIE_SECRET


    app = framework.mvc.web.Application(**settings)
    app.listen(TORNADO_PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    run(debug=True)
