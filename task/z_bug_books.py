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


def check():
    '''
        通过问题订单找出所有有问题的books记录
    '''
    pass
    # orders = db.bug.order.find({})
    # n = 0
    # for i in orders:
    #     books_list = []
    #     books = db.books.find({ "args": i._id })
    #     for b in books:
    #         if b.remark not in books_list:
    #             books_list.append(b.remark)
    #         else:
    #             db.bug.books.save(b)
    #             n += 1


def aggr():
    '''
        按用户统计涉及的金额
    '''
    books = db.bug.books.aggregate([
        {
            "$group" : {    
                "_id" : "$user",
                "count" : { "$sum" : 1 },
                "amount" : { "$sum" : "$amount" }
            }
        }
    ])
    books_list = list(books)
    for i in books_list:
        print i
        # dirc = {}
        # dirc["user"] = i._id
        # dirc["userid"] = db.user.find_one({"_id": i._id}).userid
        # dirc["count"] = i.count
        # dirc["amount"] = i.amount

        # db.bug.user.insert_one(dirc)


def export():
    '''
        导出csv
    '''
    import csv
    export_user = csv.writer(open('export_user.csv', 'wb'))
    users = db.bug.user.find()
    for i in users:
        export_user.writerow([ i.userid, i.count, round(i.amount, 2) ])

if __name__ == "__main__":
    export()