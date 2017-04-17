#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-6

import re
import os
import pymongo
import datetime
import tornado.web
from bson import ObjectId
from cuckoo import per_result
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.data.mongo import db, DBRef, Document


@url("/system/config")
class SystemConfig(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = [ "systemconfig" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        self.context.systemconfigs = [ c for c in db.systemconfig.find() ]

        return self.template()


@url("/config/(?P<key>[^/]+)/(?P<value>.+)")
class SystemConfigSet(HandlerBase):
    @tornado.web.authenticated
    def get(self, key, value):
        UP = self.context.UP
        per = [ "systemconfig" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        res_int = r"^\d+$"
        res_float = r"^\d+(\.\d+)?$"
        res_ratio = r"^\d+(\.\d+)?:\d+(\.\d+)?$"
        res_time = r"^([0-1][0-9]|2[0-3]):([0-5][0-9])$"

        float_keys = ["sim-initial-amount", "warning-single-amount", "warning-total-amount", \
            "risk-trading-amount", "oneminute-trading-amount", "pay-quota-amount", \
            "income-quota-amount", "pay-handling-percent", "pay-handling-amount", \
            "income-handling-percent", "income-handling-amount", "exchange-income-rate", \
            "exchange-pay-rate", "pay-least-amount", "income-least-amount", "order-handling-percent", \
            "goods-sale-percent"]
        time_keys = ["pay-starttime", "pay-endtime", "income-starttime", "income-endtime"]
        int_keys = [ "oneminute-trading-count", "member-status", "agent-status", "other-status" ]

        if key == "risk-pupil-ratio":
            if not re.match(res_ratio, value):
                return self.json({"status": "faild", "desc": "格式有误!"})
        elif key in int_keys:
            if not re.match(res_int, value):
                return self.json({"status": "faild", "desc": "次数必须为整数!"})
            value = int(value)
        elif key in float_keys:
            if not re.match(res_float, value):
                return self.json({"status": "faild", "desc": "格式有误!"})
            value = float(value)
        elif key in time_keys:
            if not re.match(res_time, value):
                return self.json({"status": "faild", "desc": "格式有误!"})
        elif key == "member-group":
            if value != "-1":
                try:
                    if not db.usergroup.find_one({ "_id" : ObjectId(value) }):
                        return self.json({"status": "faild", "desc": "没有此用户组!"})
                except:
                    return self.json({"status": "faild", "desc": "用户组有误!"})
        elif key == "init-referralcode":
            if value != "-1":
                if not db.user.find_one({ "referralcode" : value }):
                    return self.json({"status": "faild", "desc": "没有此推荐人!"})

        conf = db.systemconfig.find_one({ "key" : key })
        try:
            if conf:
                db.systemconfig.update({ "key" : key }, { "$set" : { "value" : value } })
            else:
                db.systemconfig.save({ "key" : key, "value" : value })

            result = self.set_cache("systemconfig", key)
            if not result:
                self.system_record("系统", 0, "系统设置", "更新缓存失败")

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "系统设置", "")
            return self.json({ "status" : "ok" })
        except Exception, e:
            print e
            self.system_record("系统", 0, "系统设置", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/system/log")
class SystemLog(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = [ "systemlog" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        key = self.get_argument("key", "")
        logtype = self.get_argument("logtype", "-1")
        receiver = self.get_argument("receiver", "")

        self.context.key = key
        self.context.logtype = logtype
        self.context.receiver = receiver
        # self.context.users = db.user.find()

        if not starttime and not endtime:
            today = self.get_date()
            self.context.starttime = today['starttime']
            self.context.endtime = today['endtime']
            self.context.show = False
            return self.template()

        where = find_where(starttime, endtime, key, logtype, receiver)
        systemlog = db.systemlog.find(where)

        self.context.systemlog = systemlog.sort([ ("createtime", -1) ]) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging = paging.parse(self)
        self.context.paging.count = self.context.systemlog.count()

        self.context.starttime = starttime
        self.context.endtime = endtime
        self.context.show = True

        return self.template()


def find_where(starttime, endtime, key="", logtype="-1", receiver=""):
    try:
        where = {}
        select_time = {}
        if starttime:
            select_time["$gt"] = datetime.datetime.strptime(starttime + ":00", "%Y-%m-%d %H:%M:%S")

        if endtime:
            select_time["$lt"] = datetime.datetime.strptime(endtime + ":59", "%Y-%m-%d %H:%M:%S")

        if select_time:
            where["createtime"] = select_time

        if logtype == "-1":
            where["logtype"] = {"$nin" : [0]}
        else:
            where["logtype"] = int(logtype)

        if key:
            where["operation"] = {"$regex" : key}

        if receiver:
            user = db.user.find_one({"userid": receiver})
            if user:
                where["user.$id"] = user._id
            else:
                where["user.$id"] = None

    except Exception, e:
        print e
        where = {}

    return where


@url("/system/log/export")
class SystemLogExport(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        return self.post()


    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = [ "systemlog" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")
        key = self.get_argument("key", "")
        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        logtype = self.get_argument("logtype", "-1")
        receiver = self.get_argument("receiver", "")

        if receiver != "":
            receiver = receiver.split(",")

        where = find_where(starttime, endtime, key, logtype, receiver)
        systemlog = db.systemlog.find(where)

        try:
            self.set_header("Content-Type", "text/csv; charset=gbk")
            self.set_header("Content-Disposition","attachment;filename=系统日志.csv")

            self.write("操作用户, 操作类型, 操作模块, 操作功能, 操作时间, IP\r\n".decode('utf8').encode('gbk'))

            kvs = {
                    1 : "登陆记录", 
                    2 : "资金变动",
                    3 : "用户操作"
            }

            for i in systemlog:
                user = i.user in ["管理员", "系统"] and i.user or i.user.fetch().username
                logtype = kvs[i.logtype]
                module = i.module
                operation = i.operation
                createtime = str(i.createtime).split(".")[0]
                ip = i.ip

                line = "{0}, {1}, {2}, {3}, {4}, {5}\n".format(user, logtype, module, operation, createtime, ip)

                self.write(line.decode('utf8').encode('gbk'))

            self.finish()
        except Exception, e:
            print e


@url("/adjust")
class Adjust(HandlerBase):

    @tornado.web.authenticated
    def books(self, user, amount, remark):
        result = db.user.find_one_and_update({"_id" : user}, {"$inc" : {"amount" : amount}}, return_document=pymongo.ReturnDocument.AFTER)

        # 增加资金流转记录
        books = {
            "user" : user,
            "amount" : amount,
            "balance" : result.amount,
            "type" : 99,
            "args" : "",
            "remark" : remark,
            "created" : datetime.datetime.utcnow()
        }
        db.books.insert_one(books)


    @tornado.web.authenticated
    def get(self):
        current_user_role = self.context.current_user_role
        if current_user_role != "admin":
            return self.redirect("/user")
        
        users = db.user.find({ "type" : 1 })
        self.context.users = users

        return self.template()


    @tornado.web.authenticated
    def post(self):
        current_user_role = self.context.current_user_role
        if current_user_role != "admin":
            return self.redirect("/user")
        current_user = self.context.current_user

        userid = self.get_argument("id", "") or None
        amount = self.get_argument("amount", "")
        remark = self.get_argument("remark", "")

        if not userid or not amount or not remark:
            return self.json({"status": "faild", "desc": "参数不全!"})
        user = db.user.find_one({ "_id" : ObjectId(userid) })
        if not user:
            return self.json({"status": "faild", "desc": "用户错误!"})

        try:
            amount = round(float(amount), 2)
        except:
            return self.json({"status": "faild", "desc": "金额格式错误!"})

        try:
            # 调整金额
            self.books(user._id, amount, remark)
            # 记录
            current_user = self.context.current_user
            self.system_record(current_user._id, 99, "资金调整", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "未知错误!"})