#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-8-15


import os
import re
import sys
import inspect
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.util import import_object, ObjectDict

import routing
from uimodule import UIModule
from requesthandler import RequestHandler

import framework.core.cache

class Application(tornado.web.Application, framework.core.cache.CacheMixin):
    """
        MVC Application
    """
    def listen(self, port, address="", **kwargs):
        """
            重写listen函数，在启动监听前先扫描RequestHandler及UIModule模块
        """
        self.settings["handler_path"] = os.path.join(os.getcwd(), self.settings.get("handler_path", ""))
        self.settings["uimodule_handler_path"] = os.path.join(os.getcwd(), self.settings.get("uimodule_handler_path", ""))
        self.settings["uimodule_template_path"] = os.path.join(os.getcwd(), self.settings.get("uimodule_template_path", ""))
        self.settings["template_path"] = os.path.join(os.getcwd(), self.settings.get("template_path", ""))

        handler_path = self.settings.get("handler_path")
        if handler_path not in sys.path:
            sys.path.insert(1, os.path.abspath(handler_path))
        self._load_handlers(os.path.abspath(handler_path))
        
        uimodule_handler_path = self.settings.get("uimodule_handler_path")
        if uimodule_handler_path not in sys.path:
            sys.path.append(os.path.abspath(uimodule_handler_path))
        self._load_uimodules(os.path.abspath(uimodule_handler_path))

        for domain, spec_list in self.handlers:
            for spec in spec_list:
                print domain.pattern, spec.regex.pattern, spec.handler_class

        if self.ui_modules:
            for k, v in self.ui_modules.items():
                print k, v

        super(Application, self).listen(port, address=address, **kwargs)


    def add_handlers(self, host_pattern, host_handlers):
        if not host_pattern.endswith("$"):
            host_pattern += "$"
        handlers = []
        
        hosts = [ h.pattern for h, s in self.handlers ]
        if host_pattern in hosts:
            handlers = [ s for h, s in self.handlers if h.pattern == host_pattern ][0]
        elif ".*$" in hosts:
            self.handlers.insert(-1, (re.compile(host_pattern), handlers))
        else:
            self.handlers.append((re.compile(host_pattern), handlers))

        for spec in host_handlers:
            if type(spec) is type(()):
                assert len(spec) in (2, 3)
                pattern = spec[0]
                handler = spec[1]

                if isinstance(handler, str):
                    handler = import_object(handler)

                if len(spec) == 3:
                    kwargs = spec[2]
                else:
                    kwargs = {}
                spec = tornado.web.URLSpec(pattern, handler, kwargs)
            handlers.append(spec)
            if spec.name:
                if spec.name in self.named_handlers:
                    logging.warning(
                        "Multiple handlers named %s; replacing previous value",
                        spec.name)
                self.named_handlers[spec.name] = spec

        if handlers:
            handlers.sort(cmp, lambda h: routing.get_order(h.handler_class), reverse=True)


    def _load_handlers(self, path):
        """
            加载RequestHandler
        """
        path = os.path.abspath(path)
        if not os.path.exists(path):
            return

        def dig(module):
            if not hasattr(module, "__dict__"):
                return

            for n, o in module.__dict__.items():
                if isinstance(o, type) and issubclass(o, RequestHandler) and not o is RequestHandler:
                    for url in routing.get_url(o):
                        self.add_handlers(".*$", ((url, o),))

        for p in os.listdir(path):
            #如果是包目录
            if os.path.exists(os.path.join(path, p, "__init__.py")):
                self._load_handlers(os.path.join(path, p))

            #如果是py文件
            elif p.endswith(".py"):
                try:
                    handler_path = self.settings.get("handler_path")
                    module_name = os.path.join(path, p[:-3]).replace(handler_path, "") \
                                .replace(os.sep, ".").strip(".")

                    module = "." in module_name and tornado.util.import_object(str(module_name)) or __import__(module_name)
                    dig(module)
                except Exception, exp:
                    print "导入{0}时出错: {1}".format(os.path.join(path, p), exp)


    def _load_uimodules(self, path):
        """
            加载UIModule模块 
        """
        path = os.path.abspath(path)
        if not os.path.exists(path):
            return

        def dig(module, ui_modules):
            if not hasattr(module, "__dict__"):
                return

            for n, o in module.__dict__.items():
                if isinstance(o, type) and issubclass(o, UIModule) and not o is UIModule:
                    ui_modules[o.__name__] = o

        for p in os.listdir(path):
            #如果是包目录
            if os.path.exists(os.path.join(path, p, "__init__.py")):
                self._load_uimodules(os.path.join(path, p))

            #如果是py文件
            elif p.endswith(".py"):
                try:
                    uimodule_handler_path = self.settings.get("uimodule_handler_path")
                    module_name = os.path.join(path, p[:-3]).replace(uimodule_handler_path, "") \
                                .replace(os.sep, ".").strip(".")

                    module = "." in module_name and tornado.util.import_object(str(module_name)) or __import__(module_name)
                    dig(module, self.ui_modules)
                except Exception, exp:
                    print "导入{0}时出错: {1}".format(os.path.join(path, p), exp)
