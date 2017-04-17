#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
import datetime
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


def books_result(user, bookstype, amount, args, remark):
    result = db.user.find_one_and_update({"_id" : user}, {"$inc" : {"amount" : amount}}, return_document=pymongo.ReturnDocument.AFTER)
    print remark
    books = {
        "user" : user,
        "amount" : amount,
        "balance" : result.amount,
        "type" : bookstype,
        "args" : args,
        "remark" : remark,
        "created" : datetime.datetime.utcnow(),
        "py": 'z_bt_bug'
    }
    db.bt.books.insert_one(books)


def repair():
    '''
        修复比特币行情停止导致的Bug
        修复内容
            6:下单, 7:结单, 8:佣金, 9:红利
            1,  下单回退(包含手续费)
            2,  佣金回退
            3,  红利回退
            4,  结单回退
        问题时间:
            ISODate("2017-03-12T07:33:52.658Z")
            ISODate("2017-03-12T08:16:31.634Z")
        数量:
            4898
    '''
    where = {}
    select_time = {}
    select_time["$gt"] = datetime.datetime.strptime("2017-03-12 07:00:00", "%Y-%m-%d %H:%M:%S")
    # select_time["$gt"] = datetime.datetime.strptime("2017-01-12 07:00:00", "%Y-%m-%d %H:%M:%S")
    select_time["$lt"] = datetime.datetime.strptime("2017-03-12 08:30:00", "%Y-%m-%d %H:%M:%S")
    where["created"] = select_time
    where['endQoute'] = 898.355
    # where['endQoute'] = 112.286

    import time
    t1 = time.time()
    orders = db.order.find(where)
    print orders.count()
    print time.time() - t1
    # for i in orders:
    #     repair_commission_position(i._id)
    #     repair_order(i._id)
    #     db.bt.order.save(i)
    #     db.order.remove({ "_id": i._id })


def repair_commission_position(order_id):
    books = db.books.find({ "args": order_id })
    for i in books:
        remark = "回退: " + i.remark
        books_result(i.user, i.type, i.amount*-1, order_id, remark)
        db.bt.books.save(i)
        db.books.remove({ "_id": i._id })


def repair_order(order_id):
    books = db.books.find({ "args": { "order": order_id } })
    for i in books:
        remark = "回退: " + i.remark
        books_result(i.user, i.type, i.amount*-1, order_id, remark)
        db.bt.books.save(i)
        db.books.remove({ "_id": i._id })



if __name__ == '__main__':
    repair()