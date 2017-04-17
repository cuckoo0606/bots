#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-11-12


import os
import inspect


def url(url = None, order = -1):
    """
        设置RequestHandler的URL地址，支持正则表达式格式，支持多URL。
        可以设置order来调整命中优先级，order值越大优先级越高。

        示例：
            @url("/index.htm")
            class IndexHandler(BaseHandler):
                def get(self):
                    pass
    """

    if url and type(url) == str:
        url = [ url ]

    def wrap(handler):
        prefix = get_prefix(handler)
        setattr(handler, "{0}_{1}".format(prefix, "url"), url)
        setattr(handler, "{0}_{1}".format(prefix, "order"), order)

        return handler

    return wrap


def get_url(handler):
    attr_name = "{0}_{1}".format(get_prefix(handler), "url")
    return hasattr(handler, attr_name) and getattr(handler, attr_name) or []


def get_order(handler):
    attr_name = "{0}_{1}".format(get_prefix(handler), "order")
    return hasattr(handler, attr_name) and getattr(handler, attr_name) or -99999999999


def get_prefix(handler):
    """
        获取属性前缀
        山寨python的私有属性实现，为属性添加前缀，防止属性值被继承
    """
    return "{0}_{1}".format(handler.__module__.replace(".", "_"), handler.__name__)
