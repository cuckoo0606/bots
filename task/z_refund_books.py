#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


def books(user, bookstype, amount, args, remark):
    result = db.user.find_one_and_update({"_id" : user}, {"$inc" : {"amount" : amount}}, return_document=pymongo.ReturnDocument.AFTER)

    books = {
        "user" : user,
        "amount" : amount,
        "balance" : result.amount,
        "type" : bookstype,
        "args" : args,
        "remark" : remark,
        "created" : datetime.datetime.utcnow(),
        "py": 'z_refund_books'
    }
    db.books.insert_one(books)


def all_orders_id():
    '''
        找出所有涉及的订单id
    '''
    try:
        orders_id = []
        sameorders = db.sameorders.find()
        for i in sameorders:
            orders = db.order.find({ "no": i.no })
            for o in orders:
                orders_id.append(o._id)
    except Exception, e:
        print e

    return orders_id


def refund():
    '''
        根据orderid找到books表的args字段
        循环所有关联订单号(25731张), 查询订单号关联的books表
        如果存在记录:
            则查询相同remark, 保留一个, 其他回退
        如果不存在记录:
            则将此单设置为未计算
    '''
    orders_id = all_orders_id()
    print len(orders_id)
    same_count = 0
    diff_count = 0
    try:
        for i in orders_id:
            remark_list = []
            result = db.books.find({ "args": i })
            if result.count() > 0:
                for b in result:
                    if b.remark not in remark_list:
                        remark_list.append(b.remark)
                    else:
                        remark = "回退: " + b.remark
                        books(b.user, b.type, b.amount*-1, i, remark)
                db.order.find_one_and_update({ "_id": i }, { "$set": { "py": 'z_refund_books' } })
                same_count += 1
            else:
                db.order.find_one_and_update({ "_id": i }, { "$unset": { "profit_process": 1, "position_process": 1 }, "$set": { "py": 'z_refund_books' } })
                diff_count += 1
        print '相同订单总数, 已回退'
        print same_count
        print '需要重算的订单总数'
        print diff_count
    except Exception, e:
        print e


if __name__ == '__main__':
    '''
        重新计算后, 需要佣金表和红利表重跑
    '''
    refund()
