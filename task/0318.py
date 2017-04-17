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

orders = db.order.find({ "status": 100 })

def check(starttime, endtime):
    '''
        找出一个订单号, 存在相同的红利记录
    '''
    o = datetime.timedelta(hours=8)
    start = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S") - o
    end = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S") - o
    select_time = {"$gte": start, "$lt": end}

    where = {}
    where["status"] = 110
    where["created"] = select_time
    orders = db.order.find(where)
    print orders.count()

    n = 0
    for i in orders:
        books_list = []
        books = db.books.find({ "args": i._id, "type": 9 })
        for b in books:
            if b.remark not in books_list:
                books_list.append(b.remark)
            else:
                db.books_position.save(b)
                n += 1

    print "相同计算的红利次数: {0}.".format(n)


if __name__ == "__main__":
    starttime = '2016-02-17 00:00:00'
    endtime = '2017-02-18 00:00:00'
    check(starttime, endtime)