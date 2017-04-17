#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')


import csv
import datetime
import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


'''
    将这批用户以及下级, 设置佣金和红利为0, 推荐码为空
'''

none_users = []

def users():
    with open('modiffy.txt') as txt:
        user_list = [ i.strip() for i in txt ]

    return user_list



def modiffy():
    user_list = users()
    import pdb
    pdb.set_trace()
    n = 0
    try:
        for i in user_list:
            user = db.user.find_one({ 'userid': i })
            if user:
                print user.relation
                modiffy_users = db.user.find({ "relation": { "$regex": user.relation } })
                print modiffy_users.count()
                for u in modiffy_users:
                    n += 1
                    # 备份
                    u["date"] = "20170316"
                    #db.user_bak_50.insert_one(u)
                    # 更新
                    #db.user.find_one_and_update({ '_id': u._id }, { '$set': { 'position': 0, 'brokerage': 0 } })
            else:
                none_users.append(i)
        print n
    except Exception as e:
        import pdb
        pdb.set_trace()
        print e

    print none_users


if __name__ == '__main__':
    modiffy()