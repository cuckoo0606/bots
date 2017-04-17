#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25


import re
import os
import datetime
import tornado.web
from bson import ObjectId
from cuckoo import per_result
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.util.security import md5
from framework.data.mongo import db, Document, DBRef


@url("/risk")
class Risk(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["riskmanage"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        key = self.get_argument("key", "")
        self.context.key = key

        where = {}
        if key:
            where["marketcode"] = {"$regex": key}

        self.context.paging = paging.parse(self)
        self.context.risk = db.risk.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.risk.count()

        return self.template()


@url("/risk/edit")
class RiskEdit(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["riskmanagea"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = ["riskmanagem"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

        self.context.risk = db.risk.find_one({"_id": ObjectId(id)})
        self.context.commoditys = db.commodity.find()

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["riskmanagea"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})
        else:
            per = ["riskmanagem"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

        marketcode = self.get_argument("marketcode", "")
        closingprice = self.get_argument("closingprice", "")
        endtime = self.get_argument("endtime", "")

        if not endtime:
            return self.json({"status": "faild", "desc": "到期时间不能为空!"})

        try:
            closingprice = float(closingprice)
            if closingprice < 0:
                return self.json({"status": "faild", "desc": "价格必须大于0!"})
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "价格格式不合法!"})

        if not marketcode:
            return self.json({"status": "faild", "desc": "行情编码不能为空!"})

        try:
            risk = Document()
            if id:
                risk = db.risk.find_one({"_id": ObjectId(id)})
                if not risk:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                risk._id = ObjectId(id)

            risk.marketcode = marketcode
            risk.closingprice = closingprice
            risk.endtime = datetime.datetime.strptime(
                endtime, "%Y-%m-%d %H:%M:%S")
            risk.createtime = datetime.datetime.now()

            db.risk.save(risk)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加风险", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加风险", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})

        return self.template()


@url("/risk/delete")
class RiskDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["riskmanaged"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        try:
            ids = self.get_argument("id", "").split(",")
            for i in ids:
                db.risk.remove({"_id": ObjectId(i)})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除风险", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除风险", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/keyaccount")
class KeyAccount(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["riskkey"]
        result = per_result(per, UP)
        if not result:
            return self.redirect("/account/signin")

        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        key = self.get_argument("key", "")
        mode = self.get_argument("mode", "4")
        receiver = self.get_arguments("receiver")
        direction = self.get_argument("direction", "2")
        autocheck = self.get_argument("autocheck", "0")
        minimum = self.get_argument("minimum", "")
        maximum = self.get_argument("maximum", "")
        usertype = self.get_argument("usertype", "0")

        self.context.starttime = starttime
        self.context.endtime = endtime
        self.context.key = key
        self.context.mode = mode
        self.context.receiver = receiver
        self.context.direction = direction
        self.context.autocheck = autocheck
        self.context.maximum = maximum
        self.context.minimum = minimum
        self.context.usertype = usertype

        try:
            s_a = db.systemconfig.find_one({"key": "warning-single-amount"})
            t_a = db.systemconfig.find_one({"key": "warning-total-amount"})
            if s_a:
                single_amount = s_a.value
            if t_a:
                total_amount = t_a.value

            try:
                if minimum:
                    minimum = float(minimum)
                    if minimum < single_amount:
                        minimum = ""
                if maximum:
                    maximum = float(maximum)
                    if maximum < single_amount:
                        maximum = ""
                if maximum < single_amount:
                    maximum = ""
            except Exception, e:
                return self.write("最大值或最小值格式错误!")

            if s_a and t_a:
                users = find_users(single_amount, total_amount, minimum, maximum, usertype)

                self.context.users = [
                    u for u in db.user.find({"_id": {"$in": users}})]

                where = get_where(starttime, endtime, key, mode,
                                  direction, receiver, [1], users)

                warehouse = db.order.find(where).sort([ ("_id", -1) ]) \
                    .skip(paging.skip(self.context.paging)) \
                    .limit(self.context.paging.size)
                ls = []

                for order in warehouse:
                    order.user = db.user.find_one({'_id': order.user})
                    ls.append(order)

                self.context.warehouse = ls
                self.context.paging = paging.parse(self)
                self.context.paging.count = db.order.find(where).count()
            else:
                self.context.users = []
                self.context.warehouse = []

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "查询重点客户", "")
            return self.template()
        except Exception, e:
            print e
            self.system_record("系统", 0, "查询重点客户", e.message)


def get_where(starttime, endtime, key, mode, direction, receiver, status, users):
    where = {}
    # 达到预警的客户

    where["status"] = {"$in": status}
    # 通过用户查询
    if receiver != [] and receiver != "":
        receivers = [ObjectId(i) for i in receiver]
        where["user"] = {"$in": receivers}
    else:
        where["user"] = {"$in": users}
    # 通过模式查询
    if mode != "4":
        where["mode"] = int(mode)

    # 通过方向查询
    if direction != "2":
        direction = int(direction)
        where["direction"] = direction

    # 通过时间查询
    select_time = {}
    o = datetime.timedelta(hours=-8)

    if starttime:
        select_time["$gt"] = datetime.datetime.strptime(
            starttime + ":00", "%Y-%m-%d %H:%M:%S") - o

    if endtime:
        select_time["$lt"] = datetime.datetime.strptime(
            endtime + ":59", "%Y-%m-%d %H:%M:%S") - o

    if select_time:
        where["created"] = select_time

    # 通过关键字查询资产或订单号
    if key:
        where["$or"] = [
            {"no": {"$regex": key}},
            {"assets.name": {"$regex": key}}
        ]

    return where


def find_users(single_amount, total_amount, minimum, maximum, usertype):
    where = {}
    if maximum:
        where["$lte"] = maximum
    if minimum:
        where["$gte"] = minimum
    else:
        where["$gt"] = single_amount

    users = [o.user for o in db.order.find(
        {"money": where, "status": 1})]

    if not maximum and not minimum:
        sale = db.order.aggregate([
            {
                "$match": {"status": 1}
            },
            {
                "$group": {
                    "_id": "$user",
                    "money": {"$sum": "$money"}
                }
            },
            {
                "$match": {"money": {"$gt": total_amount}}
            }
        ])

        for i in sale:
            users.append(i._id)

    users = list(set(users))

    if usertype == "0":
        find_users = [ i for i in users ]
    else:
        usertype = int(usertype)
        find_users = [ i for i in users if "type" in db.user.find_one({"_id" : i}) and db.user.find_one({"_id" : i}).type == usertype ]

    return find_users