#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


def check_amount():
    '''
        查询所有正式用户
        找到现在的金额和今天之前的最后一条books记录的余额
    '''
    users = db.user.find({ 'type': 1 })
    for i in users:
        books = [ b for b in db.books.find({ 'user': i._id, 'created': {"$lt" : datetime.datetime(2017,3,5)} }) ]
        if len(books) > 0:
            amount = books[0]['balance']
        else:
            amount = 0

        db.user_bak.insert_one({ '_id': i._id, 'userid': i.userid, 'init_amount': amount, 'now_amount': i.amount })


if __name__ == '__main__':
    check_amount()