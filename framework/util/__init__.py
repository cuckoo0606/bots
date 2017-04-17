#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-11-29

from tornado.util import ObjectDict
from tornado.util import import_object


class ReadonlyDict(dict):
    def __setitem__(self, name, value):
        raise Exception("只读字典不能赋值")


    def __getattr__(self, name):
        return self.__getitem__(name)


    def __setattr__(self, name, value):
        raise Exception("只读字典不能赋值")
