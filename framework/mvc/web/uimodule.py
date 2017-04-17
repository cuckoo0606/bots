#!/usr/lib/env python
#-*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-11-11

import os
import inspect
import tornado.web
import tornado.template
from tornado.util import ObjectDict


class UIModule(tornado.web.UIModule):
    """
        UI模块基类
    """

    def template(self, template_name=None, **kwargs):
        """
            输出模块模板
        """
        if not template_name:
            template_name = self.get_template_name()

        kwargs.update(self.context)
        return self.render_string(template_name, **kwargs)


    @property
    def context(self):
        return self.handler.context


    @property
    def tempdata(self):
        if not hasattr(self, "_tempdata"):
            self._tempdata = ObjectDict()

        return self._tempdata


    def get_template_name(self):
        """
            获取模块模板路径
        """

        if not hasattr(self, "_template_path"):
            module = inspect.getmodule(self.__class__)
            path = os.path.splitext(module.__file__.replace(self.request.settings.get("uimodule_handler_path"), \
                                                            self.request.settings.get("uimodule_template_path")))[0]
            self._template_path = "{0}{1}{2}.html".format(path, os.sep, self.__class__.__name__.lower())

        return self._template_path
