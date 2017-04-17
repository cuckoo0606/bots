#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2013-9-10

from tornado.util import ObjectDict


class JSONProtocol(ObjectDict):
    """
        页面处理器基类
    """
    def __init__(self, *args, **kwargs):
        super(JSONProtocol, self).__init__(*args, **kwargs)
        self.status = "ok"
        self.message = ""
        self.data = ObjectDict()
