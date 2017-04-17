#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25

import os
import re
import tornado.web
import time
import datetime
from bson import ObjectId
from cuckoo import per_result
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.data.mongo.escape import BSONEncoder
from framework.data.mongo import db, Document, DBRef

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@url("/commodity/manage")
class Commodity(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["commodityma"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        key = self.get_argument("key", "")
        self.context.key = key

        where = {}
        if key:
            where["$or"] = [{"name": {"$regex": key}},
                            {"code": {"$regex": key}}]

        self.context.paging = paging.parse(self)
        self.context.commodity = db.commodity.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.commodity.count()

        print self.request.headers['user-agent']

        return self.template()


@url("/commodity/edit")
class CommodityEdit(HandlerBase):
    """
        商品表: commodity

        名称: name
        说明: intro
        行情编码: quotation
        商品分类: classify
        分组: isgroup  0/1
    """
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["commoditymaa"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = ["commoditymam"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")

        self.context.commodity = db.commodity.find_one({"_id": ObjectId(id)})
        self.context.classify = db.classify.find()
        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["commoditymaa"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})
        else:
            per = ["commoditymam"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

        name = self.get_argument("name", "")
        intro = self.get_argument("intro", "")
        quotation = self.get_argument("quotation", "")
        classify = self.get_argument("classify", "")
        openingday = self.get_argument("openingday", "0")
        openingtime = self.get_argument("openingtime", "")
        isgroup = self.get_argument("isgroup", "")

        if not name:
            return self.json({"status": "faild", "desc": "商品名称不能为空!"})

        if not classify:
            return self.json({"status": "faild", "desc": "商品分类还没选择!"})

        if openingtime:
            time = split_time(openingtime)
            if not time:
                return self.json({"status": "faild", "desc": "开放时间格式有误!"})

        try:
            commodity = Document()
            if id:
                commodity = db.commodity.find_one({"_id": ObjectId(id)})
                if not commodity:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                commodity._id = ObjectId(id)

            commodity.name = name
            commodity.intro = intro
            commodity.quotation = quotation
            commodity.market = self.get_argument("market", "")
            commodity.code = self.get_argument("code", "")
            commodity.decimal = int(self.get_argument("decimal", "0"))
            commodity.classify = DBRef("classify", ObjectId(classify))
            commodity.openingday = int(openingday)
            commodity.openingtime = openingtime
            commodity.isgroup = isgroup
            commodity.created = datetime.datetime.now()

            db.commodity.save(commodity)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加商品", "")

            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加商品", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})
        return self.template()


def split_time(time):
    list_time = time.split(",")
    reg = r"([0-1]?\d|2[0-3]):[0-5]\d-([0-1]?\d|2[0-3]):[0-5]\d$"
    for i in list_time:
        if re.match(reg, i):
            k = i.split("-")
            if k[0] >= k[1]:
                return False
        else:
            return False
    return list_time


@url("/commodity/classify")
class classify(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["commoditycl"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        key = self.get_argument("key", "")
        self.context.key = key

        where = {}
        if key:
            where["$or"] = [{"name": {"$regex": key}},
                            {"code": {"$regex": key}}]

        self.context.paging = paging.parse(self)
        self.context.classify = db.classify.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.classify.count()
        return self.template()


@url("/commodity/classify/edit")
class classifyEdit(HandlerBase):
    """
        分类表: classify

        名称: name
        标识: code
        时间: created
    """
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["commoditycla"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = ["commodityclm"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")

        self.context.classify = db.classify.find_one({"_id": ObjectId(id)})

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["commoditycla"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})
        else:
            per = ["commodityclm"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

        code = self.get_argument("code", "")
        name = self.get_argument("name", "")

        if not name:
            return self.json({"status": "faild", "desc": "标题不能为空!"})

        if not code:
            return self.json({"status": "faild", "desc": "标识不能为空!"})

        try:
            classify = Document()
            if id:
                classify = db.classify.find_one({"_id": ObjectId(id)})
                if not classify:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                classify._id = ObjectId(id)

            classify.name = name
            classify.code = code
            classify.created = datetime.datetime.now()

            db.classify.save(classify)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加商品分类", "")

            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加商品分类", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/trade")
class Trade(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["commoditytr"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        key = self.get_argument("key", "")
        self.context.key = key

        where = {}
        if key:
            maps = {"短期期权": "0", "长期": "1", "60秒": "2", "一触即付": "3"}

            mode = -1
            for k in maps.keys():
                if key in k:
                    mode = int(maps[k])
                    break

            cs = db.commodity.find({"$or": [
                {"name": {"$regex": key}},
            ]}, {"_id": 1})

            coms = [c._id for c in cs]

            where["$or"] = [{"commodity.$id": {"$in": coms}}, {"mode": mode}]

        self.context.paging = paging.parse(self)
        self.context.trade = db.trade.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.trade.count()

        return self.template()

# 几种模式的时间格式判断
def time_select(time, type):
    '''
        0: 短期(时间点) ps : 9:30
        1: 长期(时间) ps : 29-12:00
        2: 60秒(秒数) ps : 60
    '''
    if type == 2:
        reg = r"^[1-9]\d*$"
    elif type == 0:
        reg = r"^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$"
    elif type == 1:
        reg = r"^[0-3][0-9]-([0-1]?[0-9]|2[0-3]):([0-5][0-9])$"

    result = re.match(reg, time)
    return result


def float_select(price):
    reg = r"^\d+(\.\d+)?$"
    result = re.match(reg, price)
    return result


@url("/trade/edit")
class tradeEdit(HandlerBase):
    """
        交易表: trade

        模式: mode >> 二元(0), 长期(1), 60秒(2), 一触即付(3)
        商品: commodity
        状态: status >> 开启(1), 禁用(0)
        最大值: max
        最小值: min
        设置: cycle >> 二元(多选: 每天时间点), 长期(多选: 年月日时分秒), 60秒, 一触即付
    """
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP
        mode = self.get_argument('mode', '0')
        mode = int(mode)

        if not id:
            per = ["commoditytra"]
            result = per_result(per, UP)

            commoditys = db.commodity.find()
            commodity = []

            for c in commoditys:
                e = db.trade.find(
                    {"mode": mode, "commodity.$id": ObjectId(c._id)})
                if e.count() == 0:
                    commodity.append(c)

            self.context.commoditys = commodity

            if not result:
                return self.redirect("/account/signin")
        else:
            per = ["commoditytrm"]
            result = per_result(per, UP)
            c_id = db.trade.find_one(
                {"_id": ObjectId(id)}).commodity.fetch()._id
            commodity = db.commodity.find({"_id": ObjectId(c_id)})

            self.context.commoditys = commodity

            if not result:
                return self.redirect("/account/signin")

        trade = db.trade.find_one({"_id": ObjectId(id)})
        cycles = trade and "cycle" in trade and trade.cycle or []
        new_cycles = []
        if cycles:
            for i in cycles:
                new = "{0},{1},{2}".format(i.time, i.inprice*100, i.outprice*100)
                new_cycles.append(new)

        amounts = trade and "amounts" in trade and ",".join(str(i) for i in trade.amounts)

        self.context.mode = mode
        self.context.trade = trade
        self.context.cycles = new_cycles
        self.context.amounts = amounts

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["commoditytra"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})
        else:
            per = ["commoditytrm"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

        mode = self.get_argument("mode", "")     
        commodity = self.get_argument("commodity", "")
        status = self.get_argument("status", "")
        cycle = self.get_argument("cycle", "").split("+")
        amounts = self.get_argument("amounts", "").split(",")

        if not mode:
            return self.json({"status": "faild", "desc": "交易模式不能为空!"})
        mode = int(mode)

        if not commodity:
            return self.json({"status": "faild", "desc": "商品不能为空!"})

        if not status:
            return self.json({"status": "faild", "desc": "状态码不能为空!"})

        # 周期判断
        new_cycle = []
        for i in cycle:
            if i:
                i = i.split(",")
                if len(i) != 3:
                    return self.json({"status": "faild", "desc": "周期参数错误!"})
                else:
                    time = i[0]
                    inprice = i[1]
                    outprice = i[2]
                    result_time = time_select(time, mode)
                    result_inprice = float_select(inprice)
                    result_outprice = float_select(outprice)
                    if not result_time:
                        return self.json({"status": "faild", "desc": "周期时间参数错误!"})

                    if not result_inprice:
                        return self.json({"status": "faild", "desc": "周期价内参数错误!"})

                    if not result_outprice:
                        return self.json({"status": "faild", "desc": "周期价外参数错误!"})

                    try:
                        inprice = round(float(inprice) / 100, 4)
                        outprice = round(float(outprice) / 100, 4)
                    except Exception, e:
                        return self.json({"status": "faild", "desc": "周期价格参数错误!"})

                    new_cycle.append({"time" : time, "inprice" : inprice, "outprice" : outprice})

        if not new_cycle:
            return self.json({"status": "faild", "desc": "周期参数不可留空!"})

        # 额度判断
        try:
            amounts = [int(i) for i in amounts]
        except Exception, e:
            return self.json({"status": "faild", "desc": "投资额度必须为整数!"})

        try:
            trade = Document()
            if id:
                trade = db.trade.find_one({"_id": ObjectId(id)})
                if not trade:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                trade._id = ObjectId(id)

            trade.mode = mode
            trade.commodity = DBRef("commodity", ObjectId(commodity))
            trade.assets = commodity
            trade.status = int(status)
            trade.amounts = amounts
            trade.cycle = new_cycle
            trade.createtime = datetime.datetime.now()

            db.trade.save(trade)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加交易模式", "")

            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加交易模式", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/commodity/delete")
class CommodityDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["commoditymad"]
        result = per_result(per, UP)

        if not result:
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        ids = self.get_argument("id", "").split(",")
        if not ids:
            return self.json({"status": "faild", "desc": "请选择需要删除的数据!"})

        deleted = []

        try:
            for i in ids:
                if db.trade.count({"commodity.$id": ObjectId(i)}) > 0:
                    continue

                deleted.append(i)
                db.commodity.remove({"_id": ObjectId(i)})

            if not deleted:
                return self.json({"status": "faild", "desc": "商品已被关联，未能删除!"})
            elif len(deleted) < len(ids):
                return self.json({"status": "warning", "desc": "没关联的商品已删除<br />部分商品已被关联，未能删除。"})
            else:
                return self.json({"status": "ok"})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除商品", "")
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除商品", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/commodity/classify/delete")
class classifyDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["commoditycld"]
        result = per_result(per, UP)

        if not result:
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        ids = self.get_argument("id", "").split(",")
        if not ids:
            return self.json({"status": "faild", "desc": "请选择需要删除的数据!"})

        deleted = []

        try:
            for i in ids:
                if db.commodity.count({"classify.$id": ObjectId(i)}) > 0:
                    continue

                deleted.append(i)
                db.classify.remove({"_id": ObjectId(i)})

            if not deleted:
                return self.json({"status": "faild", "desc": "商品已被关联，未能删除!"})
            elif len(deleted) < len(ids):
                return self.json({"status": "warning", "desc": "没关联的商品已删除<br />部分商品已被关联，未能删除。"})
            else:
                return self.json({"status": "ok"})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除商品分类", "")
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除商品分类", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/trade/delete")
class CommoditytradeDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["commoditytrd"]
        result = per_result(per, UP)

        if not result:
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        try:
            ids = self.get_argument("id", "").split(",")
            for i in ids:
                db.trade.remove({"_id": ObjectId(i)})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除交易模式", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除交易模式", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})
