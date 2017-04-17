#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25

import tornado.web
from bson import ObjectId
from core.web import HandlerBase
from framework.mvc.web import url
from framework.data.mongo import db
from framework.util.security import md5

try:
    from personal import PRO_ICON
except Exception, e:
    try:
        from settings import PRO_ICON
    except Exception, e:
        PRO_ICON = "icon"


@url("/account/signin")
class Signin(HandlerBase):

    def get(self):
        self.context.pro_icon = PRO_ICON
        self.context.message = ""
        self.context.next = self.get_argument("next", "")

        return self.template()

    def post(self):
        u = self.get_argument("userid", "")
        p = self.get_argument("password", "")
        r = self.get_argument("remenber", "")

        self.context.userid = u
        self.context.password = p
        self.context.pro_icon = PRO_ICON

        p = md5(p)
        user = db.user.find_one({"userid": u, "password": p})
        if user and "type" in user and user.type == 1:
            CUSTOMER = self.context.CUSTOMER
            if CUSTOMER in ["SHANDONG"]:
                role = "userrole" in user and user.userrole.fetch().roleid or None
                if not role or role == "member":
                    self.context.message = "没权限登录"
                    return self.template()
            self.set_secure_cookie(
                "u", str(user._id), expires_days=r and 7 or None)
            next = self.get_argument("next", "")
            self.system_record(user._id, 1, "用户登陆", "")
            return self.redirect(next or "/order/warehouseinpuire")
        else:
            self.context.message = "用户名或密码错误"
            return self.template()


@url("/account/signout")
class Signout(HandlerBase):

    def get(self):
        user = self.context.current_user
        self.system_record(user._id, 1, "用户注销", "")
        self.clear_cookie("u")
        return self.redirect("/account/signin")


@url("/password/modify")
class PasswordModify(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        return self.post()

    @tornado.web.authenticated
    def post(self):
        oldpwd = self.get_argument("oldpwd", "")
        firstnew = self.get_argument("firstnew", "")
        secondnew = self.get_argument("secondnew", "")

        if not oldpwd or not firstnew or not secondnew:
            return self.json({"status": "faild", "desc" : "请勿留空"})

        if firstnew != secondnew:
            return self.json({"status": "faild", "desc" : "新密码输入两次不相同"})

        current_user = self.context.current_user
        if md5(oldpwd) != current_user.password:
            return self.json({"status": "faild", "desc" : "旧密码错误"})

        db.user.find_one_and_update({ "_id" : current_user._id }, { "$set" : { "password" : md5(firstnew) } })
        self.system_record(current_user._id, 3, "修改密码", "")

        return self.json({"status": "ok"})