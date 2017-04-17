#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import pymongo
from bson import ObjectId
from framework.data.mongo import db

users_cache = {}

def get_user(userid):
    if userid in users_cache:
        return users_cache[userid]
    user = db.user.find_one({"_id": userid, "type":1})
    if user is not None:
        user = {
            "userid" : user.userid,
            "username" : user.username,
            "type" : user.type,
            "relation" : user.relation,
            "parent" : "parent" in user and user.parent and user.parent.fetch().username or "管理员"
        }
        users_cache[userid] = user
    return user

def add():
    '''
        为所有订单添加relation和userinfo
    '''
    print "order_info is start now"
    orders = db.order.find({ "relation": {"$exists" : False} })
    total = 0
    for i in orders:
        try:
            user = get_user(i.user)
            if user and user['type'] == 1:
                update = {}
                update["relation"] = user['relation']
                db.order.find_one_and_update({"_id" : i._id}, {"$set" : update})
            else:
                db.order.find_one_and_update({"_id" : i._id}, {"$set" : {"relation" : "", 'userinfo' : ''}})
        except Exception, e:
            print e
            print i._id

        total += 1
        if total % 1000 == 0:
            print total
    print 'order_info is finish'


def books():
    '''
        为所有资金表添加relation和userinfo
    '''
    print "books_infos is start now"
    books = db.books.find({ "relation": {"$exists" : False} })

    total = 0
    for i in books:
        try:
            user = get_user(i.user)
            if user and user['type'] == 1:
                update = {}
                update["relation"] = user['relation']
                db.books.find_one_and_update({"_id" : i._id}, {"$set" : update})
            else:
                db.books.find_one_and_update({"_id" : i._id}, {"$set" : {"relation" : "", 'userinfo' : ''}})
        except Exception, e:
            print e
            print i._id

        total += 1
        if total % 1000 == 0:
            print total

    print 'books_info is finish'


def deposit():
    '''
        为所有成功入金的数据添加relation
    '''
    print "deposit is start now"
    deposit = db.payment.find({ "status": 2, "relation": { "$exists": False } })

    total = 0
    for i in deposit:
        try:
            user = get_user(i.user_id)
            if user and user['type'] == 1:
                db.payment.find_one_and_update({ "_id": i._id }, { "$set": { "relation": user["relation"] } })
            else:
                db.payment.find_one_and_update({ "_id": i._id }, { "$set": { "relation": "" } })
        except Exception, e:
            print e
            print i._id

        total += 1
        if total % 1000 == 0:
            print total

    print "deposit is finish"


def outflow():
    '''
        为所有出金表添加relation
    '''
    print "outflow is start now"
    outflows = db.outflow.find({ "relation": { "$exists": False } })

    total = 0
    for i in outflows:
        try:
            user = get_user(i.user)
            if user and user['type'] == 1:
                db.outflow.find_one_and_update({ "_id": i._id }, { "$set": { "relation": user["relation"] } })
            else:
                db.outflow.find_one_and_update({ "_id": i._id }, { "$set": { "relation": "" } })
        except Exception, e:
            print e
            print i._id
        total += 1
        if total % 1000 == 0:
            print total
    print "outflow is finish"


def daily():
    '''
        为daily表添加relation
    '''
    print "daily is start now"
    dailys = db.daily.find({ "relation": { "$exists": False } })

    total = 0
    for i in dailys:
        try:
            user = get_user(i.user)
            db.daily.find_one_and_update({ "_id": i._id }, { "$set": { "relation": user["relation"] } })
        except Exception, e:
            print e
            print i._id
        total += 1
        if total % 1000 == 0:
            print total
    print "daily is finish"


if __name__ == '__main__':
    while True:
        print '开始工作'
        #add()
        books()
        #deposit()
        outflow()
        #daily()
        print '已完成'
        time.sleep(30)

