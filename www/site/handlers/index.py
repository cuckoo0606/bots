#!/usr/lib/env python
# -*- encoding:utf-8 -*-

import re
import requests
from urllib import quote
from lixingtie.web import RequestHandler, route

SERVER_DOMAIN = "http://weixin.leather-boss.com"
WECHAT_APPID = "wx3002d0a8d625f4c6"
WECHAT_APP_SECRET = "a1a0468c725f6b17d1043399ea17bb42"
WECHAT_AUTHORIZE_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base&state={2}#wechat_redirect"
WECHAT_AUTH_TOKEN_URL = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
WECHAT_USERINFO_URL = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN"


@route("/index.html")
class Index(RequestHandler):
    def get(self):
        code = self.get_argument("code", "")
        if not code and not self.get_cookie("openid"):
            url = WECHAT_AUTHORIZE_URL.format(WECHAT_APPID, quote(SERVER_DOMAIN + self.request.uri), "")
            return self.redirect(url)

        url = WECHAT_AUTH_TOKEN_URL.format(WECHAT_APPID, WECHAT_APP_SECRET, code)
        result = requests.get(url).json()
        if result and "openid" in result:
            self.set_cookie("wo", result["openid"])
            self.set_cookie("wa", result["access_token"])
            self.set_cookie("we", str(result["expires_in"]))
            self.set_cookie("wr", result["refresh_token"])
            self.set_cookie("ws", result["scope"])

        return self.view("index.html")
