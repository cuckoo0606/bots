#!/usr/lib/env python
# -*- encoding:utf-8 -*-

from lixingtie.web import Application


if __name__ == "__main__":
    Application.start(debug = True, static_path=".", views_path=".", port=8081)
