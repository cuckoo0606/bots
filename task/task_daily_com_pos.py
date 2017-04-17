#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import datetime
import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


'''
    佣金总额: commissionamounts
    佣金次数: commissionnumbers
    红利总额: bonusamounts
    红利次数: bonusnumbers

    books表, 佣金:8, 红利9
'''

users_cache = {}

def get_user(userid):
    if userid in users_cache:
        return users_cache[userid]
    user = db.user.find_one({"_id": userid, "type":1})
    user_type = user and "type" in user and user.type or 2
    users_cache[userid] = user_type
    return user_type


def get_date(created):
    delta = datetime.timedelta(hours=8)
    created = created + delta
    date = created.strftime('%Y-%m-%d')
    result = datetime.datetime.strptime(date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    return result


def statistics():
    '''
        outflow
    '''
    books = db.books.find({ "type": {"$in": [8, 9]}, "statistics": {"$exists": False} })
    print books.count()
    counts = 1
    time1 = time.time()
    try:
        for i in books:
            user_type = get_user(i.user)

            if user_type == 1:
                result = {}
                commissionamounts = 0
                commissionnumbers = 0
                bonusamounts = 0
                bonusnumbers = 0
                date = get_date(i.created)
                if i.type == 8:
                    result['commissionnumbers'] = 1
                    result['commissionamounts'] = i.amount
                else:
                    result['bonusnumbers'] = 1
                    result['bonusamounts'] = i.amount
                
                db.daily.update({ "user": i.user, 'date': date }, { "$inc": result }, True)

            db.books.find_one_and_update({ "_id": i._id }, { "$set": { "statistics": True } })

            counts += 1
            if counts % 1000 == 0:
                print counts
                print time.time() - time1
    except Exception, e:
        print e


if __name__ == '__main__':
    while True:
        statistics()
        print '已完成'
        time.sleep(30)
