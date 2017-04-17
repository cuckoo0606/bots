#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    from personal import CALCULATION_MODE, CALCULATION_CYCLE, CALCULATION_TIME
except Exception, e:
    try:
        from settings import CALCULATION_MODE, CALCULATION_CYCLE, CALCULATION_TIME
    except Exception, e:
        CALCULATION_MODE = 2
        CALCULATION_CYCLE = 1
        CALCULATION_TIME = 10

try:
    from personal import SCORE
except:
    SCORE = 1

import re
import time
import pymongo
import datetime
import schedule
from bson import ObjectId
from core.web.handlerbase import find_parents
from core.logic.new_ratio import figure_commission
from framework.data.mongo import db, Document, DBRef


def books(user, bookstype, amount, args, remark):
    new_remark = "{0}{1}元.".format(remark, amount)
    result = db.user.find_one_and_update({"_id" : user}, {"$inc" : {"amount" : amount}}, return_document=pymongo.ReturnDocument.AFTER)

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


def calculate_commission(id):
    try:
        order = db.order.find_one({"_id" : ObjectId(id)})
        if order:
            no = order.no
            order_id = order._id
            money = order.money
            user = db.user.find_one({'_id': order.user})
            if user:
                user_type = "type" in user and user.type or ""
                if user_type == 1:
                    if user.userrole.fetch().roleid != "admin":
                        user_name = user.username

                        if CALCULATION_MODE == 1:
                            users = find_parents(user, [])
                            if len(users) > 0:
                                for c_user in users:
                                    if "brokerage" in c_user and c_user.brokerage != 0:
                                        amount = round(money * c_user.brokerage / 100, 2)
                                        remark = "{0}收取ID为{1}订单号为{2}的佣金".format(c_user.username, user_name, no)
                                        books(c_user._id, 8, amount, order_id, remark)

                        else:
                            result, status, li = figure_commission(user)
                            if result:
                                for i in li:
                                    u = i[0]
                                    bro = i[3]
                                    if bro > 0:
                                        amount = round(money * bro / 100, 2)
                                        remark = "{0}收取ID为{1}的订单号为{2}的佣金".format(u.username, user_name, no)
                                        books(u._id, 8, amount, order_id, remark)
                                    else:
                                        print "佣金比例差额为小于0"
                    else:
                        print "管理员下单"
                else:
                    print "虚拟用户不参与计算"
            else:           
                print "找不到相关用户{0}的订单{1}".format(order.user, no)
        else:
            print "没有此订单{0}.".format(no)
    except Exception, e:
        print e


def job():
    try:
        where = {}
        where['status'] = {"$gte" : 1}
        where['profit_process'] = {"$exists": False}
        where['created'] = {"$gt" : datetime.datetime(2016,4,1)}
        if SCORE == -1:
            where['score'] = {"$in" : [-1, 1]}
        print '计算总数'    
        rs = db.order.find(where)
        print rs.count()

        for r in rs:
            print r._id
            try:
                calculate_commission(str(r._id))
                db.order.find_one_and_update({ "_id" : r._id }, {"$set" : {"profit_process" : True}})
            except Exception as e:
                print e
    except Exception as e:
        print e


if __name__ == "__main__":
    if CALCULATION_CYCLE == 1:
        schedule.every(CALCULATION_TIME).seconds.do(job)
    elif CALCULATION_CYCLE == 2:
        schedule.every().day.at(CALCULATION_TIME).do(job)
    elif CALCULATION_CYCLE == 3:
        if CALCULATION_TIME == 1:
            schedule.every().monday.at("04:00").do(job)
        elif CALCULATION_TIME == 2:
            schedule.every().tuesday.at("04:00").do(job)
        elif CALCULATION_TIME == 3:
            schedule.every().wednesday.at("04:00").do(job)
        elif CALCULATION_TIME == 4:
            schedule.every().thursday.at("04:00").do(job)
        elif CALCULATION_TIME == 5:
            schedule.every().friday.at("04:00").do(job)
        elif CALCULATION_TIME == 6:
            schedule.every().saturday.at("04:00").do(job)
        elif CALCULATION_TIME == 7:
            schedule.every().sunday.at("04:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)