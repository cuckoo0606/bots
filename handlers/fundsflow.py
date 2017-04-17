#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25

import os
import re
import time
import random
import pymongo
import datetime
import calendar
import tornado.web
from bson import ObjectId
from cuckoo import per_result
from core.web import HandlerBase
from core.logic.bankapply import *
from framework.web import paging
from framework.mvc.web import url, get_url
from framework.data.mongo import db, Document, DBRef

try:
    from personal import PAY_MODE
except:
    PAY_MODE = 1

try:
    from personal import PAY_TYPE
except:
    PAY_TYPE = ""


'''    
    资金表状态(1:入金, 2:入金手续费, 3:出金申请, 4:出金手续费, 5:出金失败, 6:下单, 7:结单, 8:佣金, 9:红利, 10:管理员加款, 99:系统调整)
    出金表状态(1:申请中, 2:已成功, 3:已取消, 4: 处理中, 5: 已失败, 6: 已退款, 7: 出金中, 8: 银行处理中)
'''


def books(user, bookstype, amount, args, remark):
    if bookstype == 3:
        new_remark = remark
    else:
        new_remark = "{0}{1}元.".format(remark, abs(amount))
    result = db.user.find_one_and_update({"_id" : user}, {"$inc" : {"amount" : amount}}, return_document=pymongo.ReturnDocument.AFTER)

    # 增加资金流转记录
    books = {
        "user" : user,
        "amount" : amount,
        "balance" : result.amount,
        "type" : bookstype,
        "args" : args,
        "remark" : new_remark,
        "created" : datetime.datetime.utcnow()
    }
    db.books.insert_one(books)


def today():
    """
        获取当天时间
        统计某用户当天入金金额
        统计某用户当天出金金额
        时间是否在方天时间段内
    """
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    t = "{0}-{1}-{2}".format(year, month, day)

    select_time = {}
    select_time["$gt"] = datetime.datetime.strptime(t + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    select_time["$lt"] = datetime.datetime.strptime(t + " 23:59:59", "%Y-%m-%d %H:%M:%S")
    
    return select_time


def isquota(user, amount):
    '''
        查询当天出金是否超出限额(outflow表)

        1, 得出当天限额, 需用utc时间+8小时
        2, 当天时间
        3, 当天出金金额
        4, 是否超额
    '''
    result = True
    # 系统出金额度
    quota = db.systemconfig.find_one({"key" : "pay-quota-amount"})
    quota_amount = quota and quota.value or None
    if quota_amount and quota_amount > 0:
        today = datetime.date.today()
        year = today.year
        month = today.month
        day = today.day
        t = "{0}-{1}-{2}".format(year, month, day)
        delta = datetime.timedelta(hours=8)

        select_time = {}
        select_time["$gt"] = datetime.datetime.strptime(t + " 00:00:00", "%Y-%m-%d %H:%M:%S") - delta
        select_time["$lt"] = datetime.datetime.strptime(t + " 23:59:59", "%Y-%m-%d %H:%M:%S") - delta

        where = {}
        where["created"] = select_time
        where["user"] = user
        
        pay = db.outflow.aggregate([
            {
                "$match" : where
            },
            {
                "$group" : {    
                    "_id" : -1,
                    "amount" : { "$sum" : "$amount" }
                }
            }
        ])
        list_pay = list(pay)
        pay_amount = len(list_pay) > 0 and list_pay[0].amount or 0
        if (amount + pay_amount) > quota_amount:
                result =  False

    return result


@url("/income")
class Income(HandlerBase):
    '''
        6.21更改
        入金改为加款(管理员功能)
        只加, 不扣
        管理员加款类型 : 10
    '''

    @tornado.web.authenticated
    def get(self):
        return self.template()

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = ["income"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        # 当前用户
        current_user = self.context.current_user
        current_user_id = current_user._id
        current_user_role = self.context.current_user_role
        if current_user_role != "admin":
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        amount = self.get_argument("amount", "") or 0
        receiver = self.get_argument("receiver", "")

        # 虚拟用户无法入金
        if not receiver:
            return self.json({"status": "faild", "desc": "未选中收款人!"})
        else:
            re_user = db.user.find_one({"_id" : ObjectId(receiver)})
            if not re_user:
                return self.json({"status": "faild", "desc": "未找到收款人!"})
            re_user_id = re_user._id
            receiver_type = "type" in re_user and re_user.type or None
            if receiver_type != 1:
                return self.json({"status": "faild", "desc": "此用户无法出金!"})

        # 金额判断
        try:
            amount = float(amount)
            if amount == 0:
                return self.json({"status": "faild", "desc": "充值金额不能为0!"})
            amount = round(amount, 2)
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "充值金额格式不正确!"})

        try:
            remark = "{0}为{1}加款".format(current_user.username, re_user.username)
            books(re_user_id, 10, amount, "", remark)

            self.system_record(current_user_id, 2, "管理员加款", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "管理员加款", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/pay")
class Pay(HandlerBase):
    '''
        6.21修改
        出金只有一种模式, 即出给系统
        手续费两种类型: "0"是百分比, "1"是固定值
    '''
    def eidt_no(self):
        '''
            生成两位随机大写字母+16位数字的组合
        '''
        st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        st_no = "".join(random.sample(st, 2))
        time = datetime.datetime.now().strftime("%m%d%H%M%S%f")
        no = "%s%s" % (st_no, time)

        return no


    @tornado.web.authenticated
    def get(self):
        # 显示出金手续费
        pay_type = self.redis_cache("systemconfig", "pay-handling-type")
        pay_handling_type = pay_type and pay_type.value or None
        handling_charge = 0
        if pay_handling_type:
            if pay_handling_type == "0":
                handling_percent = self.redis_cache("systemconfig", "pay-handling-percent")
                handling_charge = handling_percent and handling_percent.value or 0
                handling_charge = "{0}%".format(handling_charge)
            elif pay_handling_type == "1":
                handling_amount = self.redis_cache("systemconfig", "pay-handling-amount")
                handling_charge = handling_amount and handling_amount.value or 0               

        self.context.handling_charge = handling_charge
        return self.template()

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = ["pay"]
        result = per_result(per, UP)
        if not result:
            return self.redirect("/account/signin")

        # 出金时间限制
        pay_starttime = self.redis_cache("systemconfig", "pay-starttime")
        pay_endtime = self.redis_cache("systemconfig", "pay-endtime")
        p_start = pay_starttime and pay_starttime.value or None
        p_end = pay_endtime and pay_endtime.value or None

        now = datetime.datetime.now()
        now_time = now.strftime("%H:%M")

        if p_start:
            if now_time < p_start:
                return self.json({"status": "faild", "desc": "当前时间不在出金时间内!"})
        if p_end:
            if now_time > p_end:
                return self.json({"status": "faild", "desc": "当前时间不在出金时间内!"})

        id = self.get_argument("id", "") or None
        amount = self.get_argument("amount", "") or 0

        # 出金人(模拟用户无法出金)
        user = db.user.find_one({"_id": ObjectId(id)})
        if not user:
            return self.json({"status": "faild", "desc": "未找到出金人!"})
        usertype = "type" in user and user.type or None
        if usertype != 1:
            return self.json({"status": "faild", "desc": "此用户无法出金!"})

        user_id = user._id
        user_amount = user.amount
        username = user.username
        user_role = self.redis_cache("user", str(user_id))['roleid']
        print user_role

        # 金额判断(包括出金最小额度)
        try:
            amount = round(float(amount), 2)
            least_amount = self.redis_cache("systemconfig", "pay-least-amount")
            if least_amount:
                pay_least_amount = round(least_amount.value, 2)
                if pay_least_amount > amount:
                    return self.json({"status": "faild", "desc": "金额必须大于%s!" % str(pay_least_amount)})
            else:
                if amount <= 0:
                    return self.json({"status": "faild", "desc": "金额必须大于0!"})
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "金额格式不正确!"})

        if amount > user_amount:
            return self.json({"status": "faild", "desc": "出金人余额不足!"})

        # 当前用户
        current_user = self.context.current_user
        current_user_id = current_user._id
        current_user_name = current_user.username

        # 出金当天额度判断
        if user_role != "admin":
            result = isquota(user_id, amount)
            if not result:
                return self.json({"status": "faild", "desc": "支付方当天出金超出限额!"})
        try:
            # 手续费
            p_h_t = db.systemconfig.find_one({"key" : "pay-handling-type"})
            pay_handling_type = p_h_t and p_h_t.value or None
            handling_charge = 0
            if pay_handling_type:
                if pay_handling_type == "0":
                    handling_percent = self.redis_cache("systemconfig", "pay-handling-percent")
                    handling_charge = handling_percent and handling_percent.value or 0
                    handling_charge = round(amount * handling_charge / 100, 2)
                elif pay_handling_type == "1":
                    handling_amount = self.redis_cache("systemconfig", "pay-handling-amount")
                    handling_charge = handling_amount and handling_amount.value or 0
            '''
                出金申请表(outflow)
                user
                operator
                amount
                handling_charge
                status(1:申请中, 2:完成, 3:取消, 4: 处理中, 5: 失败)
                created
                8.14 添加单号
                8.16 添加列表日志
            '''
            outflow = Document()
            outflow.user = user_id
            outflow.operator = current_user_id
            outflow.amount = amount
            outflow.handling_charge = handling_charge
            outflow.status = 1
            outflow.no = self.eidt_no()
            outflow.created = datetime.datetime.utcnow()
            outflow.log = [
                { "addon" : datetime.datetime.utcnow(), "desc" : "成功提交出金申请!", "operator" : current_user_name }
            ]
            db.outflow.save(outflow)

            # 出金申请, 类型3
            # 更改remark
            remark = "操作人 : {0}, {1}申请出金{2}元, 手续费{3}元, 实际出金{4}元.".format(current_user_name, \
                username, amount, handling_charge, amount - handling_charge)
            books(user_id, 3, amount * -1, "", remark)

            # 记录
            self.system_record(current_user_id, 2, "用户出金申请", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "用户出金申请", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/incomereport")
class IncomeReport(HandlerBase):

    @tornado.web.authenticated
    def where_income(self, starttime, endtime, receiver, subordinate):
        where = {}
        where["status"] = 2
        select_time = self.select_time("timestamp", starttime, endtime, 8)
        if select_time:
            where["create_time"] = select_time
        where["relation"] = self.where_relation(receiver, subordinate)
        return where

    @tornado.web.authenticated
    def subordinate_income(self, where):
        income = db.payment.aggregate([
            {
                "$match" : where
            },
            {
                "$group" : {    
                    "_id" : -1,
                    "count" : { "$sum" : 1 },
                    "amount" : { "$sum" : "$fee" }
                }
            }
        ])
        income = list(income)
        return income

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["incomereport"]
        result = per_result(per, UP)
        if not result:
            return self.redirect("/account/signin")

        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        receiver = self.get_argument("receiver", "")
        subordinate = self.get_argument("subordinate", "")
        statistics = self.get_argument("statistics", "-1")

        self.context.receiver = receiver
        self.context.subordinate = subordinate
        self.context.statistics = statistics

        rendering = self.is_rendering(starttime, endtime)
        if not rendering:
            return self.template()

        where = self.where_income(starttime, endtime, receiver, subordinate)
        books = db.payment.find(where).sort([ ("create_time", -1) ]) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        result = []
        o = datetime.timedelta(hours=8)
        for i in books:
            i.user_infos = self.redis_cache("user", i.user_id)
            local_time = time.localtime(i.create_time / 1000)
            i.created = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
            result.append(i)

        self.context.books = result
        self.context.paging = paging.parse(self)
        self.context.paging.count = books.count()

        income = None
        if statistics == "1":
            income = self.subordinate_income(where)
            income = income and income[0] or None
        self.context.income = income
        return self.template()

    @tornado.web.authenticated
    def post(self):
        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        receiver = self.get_argument("receiver", "")
        subordinate = self.get_argument("subordinate", "")

        if not starttime and not endtime:
            return self.redirect("/incomereport")
        where = self.where_income(starttime, endtime, receiver, subordinate)
        books = db.payment.find(where).sort([("create_time", -1)])

        try:
            self.set_header("Content-Type", "text/csv; charset=gbk")
            self.set_header("Content-Disposition","attachment;filename=入金报表.csv")
            self.write("入金用户, 代理商, 入金金额, 申请时间\r\n".decode('utf8').encode('gbk'))

            for i in books:
                user_infos = self.redis_cache("user", i.user_id)
                user = user_infos.userid + "【" + user_infos.username + "】"
                parent = user_infos.parent_infos['userid'] + "【" + user_infos.parent_infos['username'] + "】"
                local_time = time.localtime(i.create_time / 1000)
                created = time.strftime('%Y-%m-%d %H:%M:%S', local_time)

                line = "%s, %s, %s, %s\n" % (user, parent, i.fee, created)
                self.write(line.decode('utf8').encode('gbk'))
            self.finish()
        except Exception, e:
            print e


@url("/payreport")
class PayReport(HandlerBase):

    @tornado.web.authenticated
    def subordinate_pay(self, where):
        pay_list = []
        try:
            pay = db.outflow.aggregate([
                {
                    "$match" : where
                },
                {
                    "$group" : {    
                        "_id" : "$status",
                        "count" : { "$sum" : 1 },
                        "amount" : { "$sum" : "$amount" },
                        "handling_charge" : { "$sum" : "$handling_charge" }
                    }
                }
            ])
            pay = list(pay)
            if pay:
                for i in pay:
                    pay_list.append({"status" : i._id, "count" : i.count, "amount" : i.amount, "handling_charge" : i.handling_charge})

            return pay_list
        except Exception, e:
            print e
            return []

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["payreport"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        status = self.get_argument("status", "")
        receiver = self.get_argument("receiver", "")
        subordinate = self.get_argument("subordinate", "")
        statistics = self.get_argument("statistics", "-1")

        self.context.status = status
        self.context.receiver = receiver
        self.context.subordinate = subordinate
        self.context.statistics = statistics

        rendering = self.is_rendering(starttime, endtime)
        if not rendering:
            return self.template()

        where = self.where_outflow(starttime, endtime, receiver, subordinate, status)
        print where
        outflow = db.outflow.find(where).sort([ ("created", -1) ]) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)

        result_outflow = self.userinofs_lists(outflow)
        self.context.outflow = result_outflow
        self.context.paging = paging.parse(self)
        self.context.paging.count = outflow.count()
        self.context.current_user_id = self.context.current_user._id

        # 统计
        pay_list = None
        if statistics == "1":
            pay_list = self.subordinate_pay(where)
        self.context.pay_list = pay_list

        return self.template()

    
    @tornado.web.authenticated
    def post(self):
        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        status = self.get_argument("status", "")
        receiver = self.get_argument("receiver", "")
        subordinate = self.get_argument("subordinate", "")

        if not starttime and not endtime:
            return self.redirect("/payreport")

        reg = self.get_lower_user()
        current_user = self.context.current_user
        where = self.where_outflow(starttime, endtime, receiver, subordinate, status)
        outflow = db.outflow.find(where).sort([("created", -1)])

        try:
            self.set_header("Content-Type", "text/csv; charset=gbk")
            self.set_header("Content-Disposition","attachment;filename=出金报表.csv")

            users = [ u for u in db.user.find() ]
            dicts = {}
            for i in users:
                dicts[i._id] = "{0}【{1}】".format(i.userid, i.username)

            self.write("资金单号, 出金用户, 出金金额, 手续费, 实际金额, 申请状态, 申请时间\r\n".decode('utf8').encode('gbk'))
            kvs = {1:"申请中", 2:"已成功", 3:"已取消", 4:"处理中", 5:"已失败", 6:"已退款", 7:"出金中", 8:"银行处理"}

            o = datetime.timedelta(hours=8)
            for r in outflow:
                no = "no" in r and r.no or "未知单号"
                user = r.user in dicts and dicts[r.user] or "未知用户"
                amount = round(r.amount, 2)
                handling_charge = "handling_charge" in r and round(r.handling_charge, 2) or 0
                status = 'status' in r and kvs[r.status] or "未知状态"
                created = str(r.created+o).split(".")[0]

                pay_rate = self.context.exchange_pay_rate
                real_amount = round((amount-handling_charge)*pay_rate, 2)

                line = "%s, %s, %f, %f, %f, %s, %s\n" \
                        % (no, user, amount, handling_charge, real_amount, status, created)
                self.write(line.decode('utf8').encode('gbk'))
            self.finish()
        except Exception, e:
            print e


@url("/confirm")
class Confirm(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["confirm"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        receiver = self.get_argument("receiver", "")
        '''
            是否需要
        '''
        page = self.get_argument("page", "")
        self.context.page = page
        self.context.receiver = receiver
        rendering = self.is_rendering(starttime, endtime)
        if not rendering:
            return self.template()

        current_user = self.context.current_user
        where = self.where_outflow(starttime, endtime, receiver, "", 1)

        outflow = db.outflow.find(where).sort([ ("created", -1) ]) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)

        self.context.outflow = outflow
        self.context.paging = paging.parse(self)
        self.context.paging.count = outflow.count()

        return self.template()

    @tornado.web.authenticated
    def post(self):
        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        receiver = self.get_argument("receiver", "")

        if not starttime and not endtime:
            return self.redirect("/confirm")

        current_user = self.context.current_user
        where = self.where_outflow(starttime, endtime, receiver, "", 1)
        outflow = db.outflow.find(where).sort([("created", -1)])

        try:
            self.set_header("Content-Type", "text/csv; charset=gbk")
            self.set_header("Content-Disposition","attachment;filename=资金确认报表.csv")
            self.write("订单号, 用户id, 用户名称, 金额, 手续费, 实际金额, 银行, 支行, 开户人, 银行账号, 省份, 城市, 手机号码, 时间\r\n".decode('utf8').encode('gbk'))

            kvs = {"CEEBBANK":"中国光大银行", "ABC":"中国农业银行", "BOC":"中国银行", "BOCOM":"交通银行", "CCB":"中国建设银行", "ICBC":"中国工商银行", \
                "PSBC":"中国邮政储蓄银行", "CMBC":"招商银行", "SPDB":"浦发银行", "CEBBANK":"中国光大银行", "ECITIC":"中信银行", "PINGAN":"平安银行", \
                "CMBCS":"中国民生银行", "HXB":"华夏银行", "CGB":"广发银行", "CIB":"兴业银行", "HSB":"徽商银行", "CSCB":"长沙银行", "ZJRCC":"浙江省农村信用社联合社"}
            for i in outflow:
                # user = self.redis_cache("user", str(i.user))
                user = db.user.find_one({ "_id": i.user })
                userid = user and "userid" in user and user.userid or ""
                username = user and "username" in user and user.username or ""
                bank = user and "bank" in user and user.bank and kvs[user.bank] or ""
                bankbranch = user and "bankbranch" in user and user.bankbranch or ""
                bankholder = user and "bankholder" in user and user.bankholder or ""
                bankaccount = user and "bankaccount" in user and user.bankaccount or ""
                province = user and "province" in user and user.province or ""
                city = user and "city" in user and user.city or ""
                phone = user and 'phone' in user and user.phone or ""
                amount = "amount" in i and str(i.amount) or "0"
                handling_charge = "handling_charge" in i and str(i.handling_charge) or "0"
                created = (i.created + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                pay_rate = self.context.exchange_pay_rate
                real_amount = str(round((float(amount)-float(handling_charge))*pay_rate, 2))

                line = "\t%s, \t%s, \t%s, %s, %s, %s, %s, %s, %s, \t%s, %s, %s, \t%s, %s\n" \
                        % (i.no, userid, username, amount, handling_charge, real_amount, bank, bankbranch, bankholder, \
                            bankaccount, province, city, phone, created)
                self.write(line.decode('utf8').encode('gbk'))
            self.finish()
        except Exception, e:
            print e


@url("/confirm/detail")
class ConfirmDetail(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        if not id:
            return self.redirect("/confirm")
        outflow = db.outflow.find_one({"_id" : ObjectId(id)})
        if not outflow:
            return self.redirect("/confirm")

        user = db.user.find_one({"_id" : outflow.user})
        if not user:
            return self.redirect("/confirm")

        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        receiver = self.get_argument("receiver", "")
        page = self.get_argument("page", "")
        self.context.starttime = starttime
        self.context.endtime = endtime
        self.context.receiver = receiver
        self.context.page = page

        # 出金汇率
        pay_rate = self.redis_cache("systemconfig", "exchange-pay-rate")
        exchange_pay_rate = pay_rate and pay_rate.value or 0

        handling_charge = "handling_charge" in outflow and outflow.handling_charge or 0
        pay_amount = pay_rate and round((outflow.amount-handling_charge) * exchange_pay_rate, 2) or outflow.amount

        self.context.user = user
        self.context.outflow = outflow
        self.context.pay_amount = pay_amount
        self.context.exchange_pay_rate = exchange_pay_rate

        return self.template()


@url("/confirm/pay")
class ConfirmPay(HandlerBase):
    '''
        确认出金(计算实际出金人民币)
        判断出金手续费, 若用户不够钱即失败
        分模式: 1: 旧模式. 2: 新模式
    '''
    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = ["confirm"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        id = self.get_argument("id", "") or None
        if not id:
            return self.json({"status": "faild", "desc": "未找到该出金记录!"})

        outflow = db.outflow.find_one({"_id": ObjectId(id)})
        if not outflow:
            return self.json({"status": "faild", "desc": "未找到该出金记录!"})

        if outflow.status != 1:
            return self.json({"status": "faild", "desc": "该订单异常!"})

        current_user = self.context.current_user
        current_user_id = current_user._id
        current_user_role = self.context.current_user_role
        if current_user_role != "admin":
            return self.json({"status": "faild", "desc": "只有管理员能处理该出金记录!"})

        user = db.user.find_one({"_id" : outflow.user})
        if not user:
            return self.json({"status": "faild", "desc": "出金用户异常!"})
        user_amount = user.amount

        '''
            判断用户的银行信息是否齐全
        '''
        try:
            bankholder = "bankholder" in user and user.bankholder or ""
            bank = "bank" in user and user.bank or ""
            bankbranch = "bankbranch" in user and user.bankbranch or ""
            bankaccount = "bankaccount" in user and user.bankaccount or ""
            province = "province" in user and user.province or ""
            city = "city" in user and user.city or ""
            bankId = 'bankId' in user and user.bankId or ""
            if not bankholder or not bank or not bankbranch or not bankaccount:
                return self.json({"status": "faild", "desc": "用户银行信息不全!"})
        except:
            return self.json({"status": "faild", "desc": "用户银行信息不全!"})

        '''
            出金模式:
                1: 不需要银行处理, 直接确认
                2: 需要银行处理 
        '''
        try:
            logs = "log" in outflow and outflow.log or []
            if PAY_MODE == 1:
                # 出金申请表状态改为完成, 添加日志
                logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "出金成功!", "operator" : current_user.username })
                db.outflow.find_one_and_update({ "_id" : outflow._id }, { "$set" : { "status" : 2, "log" : logs } })

                self.system_record(current_user_id, 2, "出金确认", "")
                return self.json({"status": "ok"})
            else:
                # 初始化出金提交状态
                pay_status = -1
                # 按客户, 提交转账申请
                if not PAY_TYPE:
                    return self.json({"status": "faild", "desc": "无法确认商户出金类型!"})
                
                # 汇潮出金
                if PAY_TYPE == 1:
                    if not province or not city:
                        return self.json({"status": "faild", "desc": "银行卡省份和城市不能为空!"})

                    # 判断银行类型
                    banks = {
                        "ABC" : "农业银行",
                        "ICBC" : "工商银行",
                        "BOCOM" : "交通银行",
                        "CGB" : "广东发展银行",
                        "CCB" : "建设银行",
                        "SPDB" : "上海浦东发展银行",
                        "CMBC" : "招商银行",
                        "CMBCS" : "中国民生银行",
                        "CIB" : "兴业银行",
                        "ECITIC" : "中信银行",
                        "HXB" : "华夏银行",
                        "CEBBANK" : "中国光大银行",
                        "PINGAN" : "平安银行",
                        "PSBC" : "中国邮政储蓄银行"
                    }
                    bankName = bank in banks and banks[bank] or None
                    if not bankName:
                        return self.json({"status": "faild", "desc": "暂不支持此银行的出金!"})
                    else:
                        pay_status = 1
                        user.bankName = bankName
                
                # 通联出金
                elif PAY_TYPE == 2:
                    bankcode = {
                        "ICBC" : "102",
                        "ABC" : "103",
                        "BOC" : "104",
                        "CCB" : "105",
                        "BOCOM" : "301",
                        "ECITIC" : "302",
                        "CEBBANK" : "303",
                        "HXB" : "304",
                        "CMBCS" : "305",
                        "CGB" : "306",
                        "CMBC" : "308",
                        "CIB" : "309",
                        "SPDB" : "310",
                        "HSB" : "319",
                        "PSBC" : "403"
                    }

                    banknames = {
                        "102" : "中国工商银行",
                        "103" : "中国农业银行",
                        "104" : "中国银行",
                        "105" : "中国建设银行",
                        "301" : "交通银行",
                        "302" : "中信银行",
                        "303" : "中国光大银行",
                        "304" : "华夏银行",
                        "305" : "中国民生银行",
                        "306" : "广东发展银行",
                        "308" : "招商银行",
                        "309" : "兴业银行",
                        "310" : "上海浦东发展银行",
                        "319" : "徽商银行",
                        "403" : "中国邮政储蓄银行"
                    }

                    bankNo = bank in bankcode and bankcode[bank] or ""
                    bankName = bankNo and bankNo in banknames and banknames[bankNo] or ""
                    
                    if not bankNo or not bankName:
                        return self.json({"status": "faild", "desc": "无法或者有效的银行编号!"})
                    else:
                        pay_status = 1
                        user.bankNo = bankNo
                        user.bankName = bankName

                # 开联出金
                elif PAY_TYPE == 3:
                    banks = {
                        "ABC": "农业银行",
                        "ICBC": "工商银行",
                        "BOCOM": "交通银行",
                        "CGB": "广发银行",
                        "CCB": "建设银行",
                        "SPDB": "上海浦东发展银行",
                        "CMBC": "招商银行",
                        "CMBCS": "中国民生银行",
                        "CIB": "兴业银行",
                        "ECITIC": "中信银行",
                        "HXB": "华夏银行",
                        "CEBBANK": "中国光大银行",
                        "PINGAN": "平安银行",
                        "PSBC": "中国邮政储蓄银行"
                    }
                    bankName = bank in banks and banks[bank] or ""

                    if not bankId:
                        return self.json({"status": "faild", "desc": "开户行行号不能为空!"})
                    else:
                        pay_status = 1
                        user.bankName = bankName

                else:
                    return self.json({"status": "faild", "desc": "未明的商户, 请联系管理员!"})

                # 如果提交出金成功, 则计算实际出金金额
                if pay_status == 1:
                    # 实际出金金额(金额 * 出金汇率)
                    pay_rate = db.systemconfig.find_one({"key" : "exchange-pay-rate"})
                    exchange_pay_rate = pay_rate and pay_rate.value or 0 

                    # 2017-3-31更改
                    handling_charge = "handling_charge" in outflow and outflow.handling_charge or 0
                    pay_amount = exchange_pay_rate > 0 and round((outflow.amount-handling_charge) * exchange_pay_rate, 2) or outflow.amount

                    # 状态改为处理中
                    desc = "出金汇率: {0}, 实际出金人民币{1}元!".format(exchange_pay_rate, pay_amount)
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : desc, "operator" : current_user.username })
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "正在处理中, 请耐心等候!",\
                        "operator" : current_user.username })
                    db.outflow.find_one_and_update({ "_id" : outflow._id }, { "$set" : { "status" : 4, "log" : logs,\
                        "user_bak" : user, "pay_amount" : pay_amount } })
                    return self.json({"status": "ok", "desc": "正在提交申请"})

        except Exception, e:
            self.system_record("系统", 0, "出金确认", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/cancel/pay")
class CancelPay(HandlerBase):

    '''
        将手动取消的订单的状态由申请中(状态1)改为已取消(状态3)
    '''

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = ["confirm"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        id = self.get_argument("id", "") or None
        if not id:
            return self.json({"status": "faild", "desc": "未找到该出金记录!"})

        outflow = db.outflow.find_one({"_id": ObjectId(id)})
        if not outflow:
            return self.json({"status": "faild", "desc": "未找到该出金记录!"})

        if outflow.status != 1:
            return self.json({"status": "faild", "desc": "该订单异常!"})

        current_user = self.context.current_user
        current_user_id = current_user._id
        current_user_role = self.context.current_user_role
        if current_user_role != "admin":
            return self.json({"status": "faild", "desc": "只有管理员能处理该出金记录!"})

        user = db.user.find_one({"_id" : outflow.user})
        if not user:
            return self.json({"status": "faild", "desc": "出金用户异常!"})

        try:
            # 出金申请表状态改为失败
            logs = "log" in outflow and outflow.log or []
            logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "出金已取消!", "operator" : current_user.username })
            db.outflow.find_one_and_update({ "_id" : outflow._id }, { "$set" : { "status" : 3, "log" : logs } })
            # 返钱给出金用户
            remark = "出金取消, 返还{0}用户".format(user.username)
            books(user._id, 5, outflow.amount, outflow._id, remark)
            self.system_record(current_user_id, 2, "出金取消", "")
            return self.json({"status": "ok"})
        except Exception, e:
            self.system_record("系统", 0, "出金取消", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/outflowview")
class OutflowView(HandlerBase):

    '''
        资金流水详情
    '''
    @tornado.web.authenticated
    def get(self):
        outflowid = self.get_argument("outflowid", "") or None
        outflow = db.outflow.find_one({ "_id" : ObjectId(outflowid) })

        self.context.outflow = outflow

        return self.template()


@url("/outflow/refund")
class OutflowRefund(HandlerBase):
    '''
        失败订单退款
        管理员权限
    '''
    @tornado.web.authenticated
    def post(self):
        current_user_role = self.context.current_user_role
        if current_user_role != "admin":
            return self.json({"status": "faild", "desc": "没此权限!"})

        outflowid = self.get_argument("outflowid", "") or None
        outflow = db.outflow.find_one({ "_id" : ObjectId(outflowid) })
        if not outflow:
            return self.json({"status": "faild", "desc": "未找到此订单!"})

        if outflow.status != 5:
            return self.json({"status": "faild", "desc": "订单状态异常!"})

        current_user = self.context.current_user
        try:
            # 订单状态由已失败转为已退款(5改6)
            logs = outflow.log
            logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "已退款!", "operator" : current_user.username })
            db.outflow.find_one_and_update({ "_id" : outflow._id }, { "$set" : { "status" : 6, "log" : logs, "refund" : True } })
            # 资金回退(出金失败)
            user = db.user.find_one({ "_id" : outflow.user })
            remark = "订单: {0}出金失败, 返还{1}".format(outflow.no, user.username)
            books(user._id, 5, outflow.amount, {"no" : outflow._id}, remark)
            # 手续费回退
            handling_charge = "handling_charge" in outflow and outflow.handling_charge or 0
            if handling_charge > 0: 
                handling_remark = "订单: {0}出金失败, 返还手续费{1}"
                books(user._id, 4, handling_charge, {"no" : outflow._id}, handling_remark)
            self.system_record(current_user._id, 2, "出金退款", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/batchconfrim")
class BatchConfrim(HandlerBase):
    '''
        批量确认(2017-02-23)
        判断用户是否够手续费
    '''
    @tornado.web.authenticated
    def confirm(self, id):
        outflow = db.outflow.find_one({ "_id": ObjectId(id) })
        user = db.user.find_one({ "_id": outflow.user })

        # 出金申请表状态改为完成, 添加日志
        logs = outflow.log
        current_user = self.context.current_user
        logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "出金成功!", "operator" : current_user.username })
        db.outflow.find_one_and_update({ "_id" : outflow._id }, { "$set" : { "status" : 2, "log" : logs } })
        self.system_record(current_user._id, 2, "出金确认", "")
        return True


    @tornado.web.authenticated
    def post(self):
        if self.context.current_user_role != "admin":
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        if PAY_MODE != 1:
            return self.json({"status": "faild", "desc": "线上出金模式不能批量处理!"})

        try:
            ids = self.get_argument("id").split(",")
            if ids == [""]:
                return self.json({"status": "faild", "desc": "请选择需要删除的数据"})

            outflow_list = []
            for i in ids:
                ps = None
                outflow = db.outflow.find_one({"_id": ObjectId(i)})
                no = "no" in outflow and outflow.no or ""
                status = "status" in outflow and outflow.status or ""
                if not outflow:
                    print '没有此单号'
                    ps = "{0}: 没有此单号".format(i)
                elif status != 1:
                    print '订单状态异常'
                    ps = "{0}: 此单号状态异常".format(no)
                else:
                    result = self.confirm(i)
                if ps:
                    outflow_list.append(ps)

            self.system_record(self.context.current_user._id, 3, "批量确认出金", "")
            if len(outflow_list) >= 1:
                return self.json({"status": "warning", "desc": outflow_list})
            else:
                return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除用户", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/batchcancle")
class BatchCancle(HandlerBase):
    '''
        批量取消(2017-02-23)
    '''
    @tornado.web.authenticated
    def cancle(self, id):
        current_user = self.context.current_user
        outflow = db.outflow.find_one({ "_id": ObjectId(id) })
        user = db.user.find_one({ "_id": outflow.user })
        logs = "log" in outflow and outflow.log or []
        logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "出金已取消!", "operator" : current_user.username })
        db.outflow.find_one_and_update({ "_id" : outflow._id }, { "$set" : { "status" : 3, "log" : logs } })
        # 返钱给出金用户
        remark = "出金取消, 返还{0}用户".format(user.username)
        books(user._id, 5, outflow.amount, outflow._id, remark)
        self.system_record(current_user._id, 2, "出金取消", "")
        
        return True


    @tornado.web.authenticated
    def post(self):
        if self.context.current_user_role != "admin":
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        if PAY_MODE != 1:
            return self.json({"status": "faild", "desc": "线上出金模式不能批量处理!"})

        try:
            ids = self.get_argument("id").split(",")
            if ids == [""]:
                return self.json({"status": "faild", "desc": "请选择需要删除的数据"})

            outflow_list = []
            for i in ids:
                ps = None
                outflow = db.outflow.find_one({"_id": ObjectId(i)})
                no = "no" in outflow and outflow.no or ""
                status = "status" in outflow and outflow.status or ""
                if not outflow:
                    print '没有此单号'
                    ps = "{0}: 没有此单号".format(i)
                elif status != 1:
                    print '订单状态异常'
                    ps = "{0}: 此单号状态异常".format(no)
                else:
                    self.cancle(i)
                
                if ps:
                    outflow_list.append(ps)

            self.system_record(self.context.current_user._id, 3, "批量确认出金", "")
            if len(outflow_list) >= 1:
                return self.json({"status": "warning", "desc": outflow_list})
            else:
                return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除用户", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})
