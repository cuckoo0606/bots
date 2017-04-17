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
        "py": 'z_bug_refund'
    }
    db.books.insert_one(books)


def refund():
    '''
        在bug.books表里回退
    '''
    books = db.bug.books.find({ "rerund": {"$exists": False} })
    print books.count()
    n = 0
    try:
        for i in books:
            remark = "回退: {0}".format(i.remark)
            n += 1
            #books(i.user, i.type, i.amount*-1, i._id, remark)
    except Exception, e:
        print e

    print n


if __name__ == '__main__':
    refund()
