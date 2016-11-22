#!/usr/lib/env python
# -*- encoding:utf-8 -*-

import re
import requests
from urllib import quote
from core.wechat import *
from settings import SERVER_DOMAIN
from lixingtie.web import RequestHandler, route


@route("/index.html")
class Index(RequestHandler):
    def get(self):
        #api = WeChatPay()
        #code = self.get_argument("code", "")
        #if not code and not self.get_cookie("openid"):
        #    url = api.get_auth_url(quote(SERVER_DOMAIN + self.request.uri), "")
        #    return self.redirect(url)
        #
        #result = api.get_openid(code)
        #if result and "openid" in result:
        #    self.set_cookie("wo", result["openid"])
        #    self.set_cookie("wa", result["access_token"])
        #    self.set_cookie("we", str(result["expires_in"]))
        #    self.set_cookie("wr", result["refresh_token"])
        #    self.set_cookie("ws", result["scope"])

        return self.view("index.html")
