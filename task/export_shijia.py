#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
import csv
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef

'''
    恒亿结算
    导出所有用户的余额, 入金次数, 入金总额, 出金次数, 出金总额, 佣金, 红利
'''
users = [u._id for u in  db.user.find({ "type": 1 })]
export_cvs = csv.writer(open('export.csv', 'wb'))
export_cvs.writerow([ '用户'.decode('utf8').encode('gbk'), '代理商'.decode('utf8').encode('gbk'), '入金总额'.decode('utf8').encode('gbk'), \
        '入金次数'.decode('utf8').encode('gbk'), '出金总额'.decode('utf8').encode('gbk'), '出金次数'.decode('utf8').encode('gbk'), \
        '佣金'.decode('utf8').encode('gbk'), '红利'.decode('utf8').encode('gbk'), '余额'.decode('utf8').encode('gbk') ])

def aggr():

    find_books = db.books.aggregate([
        {
            "$group": {
                "_id": {"user": "$user", "type": "$type"},
                "count": {"$sum": 1},
                "amount": {"$sum": "$amount"}
            }
        }
    ])
    books = list(find_books)
    for u in users:
        in_amount = 0
        in_count = 0
        pay_amount = 0
        pay_count = 0
        position = 0
        commission = 0

        # 余额
        current_user = db.user.find_one({"_id" : u})
        c_amount = current_user.amount
        # 出金次数和金额
        find_pays = db.outflow.aggregate([
            {
            "$match": {"user": u, "status": 2}
            },
            {
            "$group": {
                "_id": -1,
                "count": {"$sum": 1},
                "amount": {"$sum": "$amount"}
                }
            }
        ])
        list_pays = list(find_pays)
        if len(list_pays) > 0:
            pay_amount = list_pays[0]["amount"]
            pay_count = list_pays[0]["count"]


        dicts = Document()
        for b in books:
            # 入金统计
            if b._id.type == 1:
                if b._id.user == u:
                    in_amount += b.amount
                    in_count += b.count

            # 佣金统计
            if b._id.type == 8:
                if b._id.user == u:
                    commission += b.amount

            # 头寸统计
            if b._id.type == 9:
                if b._id.user == u:
                    position += b.amount

        user = '{0} [{1}]'.format(current_user.userid, current_user.username) 
        agent = "parent" in current_user and current_user.parent and current_user.parent.fetch().username or ""

        export_cvs.writerow([ user.decode('utf8').encode('gbk'), agent.decode('utf8').encode('gbk'), round(in_amount, 2), \
            in_count, round(pay_amount, 2), pay_count, round(commission, 2), round(position, 2), round(c_amount) ])


if __name__ == "__main__":
    books = aggr()