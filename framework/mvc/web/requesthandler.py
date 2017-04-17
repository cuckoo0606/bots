#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-8-15

import os
import sys
import json
import inspect
import tornado.web
import tornado.escape

from routing import url
from tornado.util import ObjectDict
from session import Session, RedisSession


class RequestHandler(tornado.web.RequestHandler):
    """
        MVC RequestHandler

        示例：
            @url("/index")
            class HandlerUrl(RequestHandler):
                def get(self):
                    return self.content("这是一个自定义Handler匹配URL的例子")

    """

    @property
    def tempdata(self):
        if not hasattr(self, "_tempdata"):
            self._tempdata = ObjectDict()

        return self._tempdata


    @property
    def context(self):
        """
            请求上下文
            数据存放到上下文后，handler以及uimodule可以通过self.context访问数据，实现请求数据共享
            在上下文里的数据，在模板文件可以直接通过key访问(只有通过handler或module的view函数输出的模板)
            当context里的数据和调用view函数时传的参数冲突时，以context里的数据优先。
            e.g.:
            index.py
                self.context["page_title"] = "网易"
            index.html
                <title>{{ page_title }}</title>
        """
        if not hasattr(self, "_context"):
            self._context = ObjectDict()

        return self._context


    def prepare(self):
        """
            处理前执行代码
        """
        if "debug" in self.settings and self.settings["debug"]:
            print "{0} {1} {2}".format(self.request.method, self.request.path, self)


    def content(self, content, content_type="text/plain; charset=utf-8"):
        """
            输出文本到页面
        """
        self.set_header("Content-Type", content_type)
        self.write(content)


    def json(self, obj, content_type="text/javascript; charset=utf-8", cls=None):
        """
            输出json结果
        """
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls).replace("</", "<\\/"))


    def file(self, path, content_type="application/x-octet-stream"):
        """
            输出文件
        """
        if path and os.path.isfile(path) and os.path.exists(path):
            with open(path) as f:
                self.set_header("Content-Type", content_type)
                self.write(f.read())

            self.finish()

        return self.set_status(404)


    def template(self, template_name=None, **kwargs):
        """
            返回页面模板
        """
        if not template_name:
            template_name = self.get_template_name()

        if not template_name:
            return self.set_status(404)

        template_name = os.path.join(self.settings.get("template_path", ""), template_name)

        kwargs.update(self.context)

        template_name = os.path.abspath(template_name)
        if os.path.exists(template_name) and os.path.isfile(template_name):
            return self.render(template_name, **kwargs)
        else:
            print "找不到模板页:" + template_name
            return self.set_status(404)


    def get_template_name(self):
        """
            获取模板路径
        """

        if hasattr(self, "_template_name"):
            return self._template_name

        module = inspect.getmodule(self.__class__)
        path = os.path.splitext(module.__file__.replace(self.settings.get("handler_path"), self.settings.get("template_path")))[0]
        self._template_name = "{0}{1}{2}.html".format(path, os.sep, self.__class__.__name__.lower())

        if os.path.exists(self._template_name):
            return self._template_name

        bases = self.__class__.__bases__;
        for parent in bases:
            module = inspect.getmodule(parent.__class__)
            if not module or not hasattr(module, "__file__"):
                continue

            base_path = os.path.splitext(module.__file__.replace(self.settings.get("handler_path"), self.settings.get("template_path")))[0]
            base_path = "{0}{1}{2}.html".format(path, os.sep, parent.__class__.__name__.lower())

            if base_path and os.path.exists(base_path):
                self._template_name = base_path
                return self._template_name
        
        return self._template_name


    @property
    def session(self):
        """
            获取会话数据
        """

        if hasattr(self, '_session'):
            return self._session
        else:
            expires = self.settings.get('permanent_session_lifetime') or 30

            if self.settings.get('session_redis'):
                self._session = RedisSession(self, host=self.settings["session_redis"]["host"],
                                             port=self.settings["session_redis"]["port"], expires=expires)
            else:
                self._session = Session(self, expires=expires)

            return self._session


    @property
    def cache(self):
        return self.application.cache
