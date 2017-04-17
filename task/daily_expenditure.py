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
    出金成功次数: expenditure_numbers
    出金成功总额: expenditure_amounts

    出金表状态(1:申请中, 2:已成功, 3:已取消, 4: 处理中, 5: 已失败, 6: 已退款, 7: 出金中, 8: 银行处理中)
    只统计已成功的数据, 像通联那些不管
'''

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
    outflows = db.outflow.find({ "status": 2, "statistics": {"$exists": False} })
    print outflows.count()

    counts = 1
    time1 = time.time()
    try:
        for i in outflows:
            user = db.user.find_one({ "_id": i.user })
            user_type = user and "type" in user and user.type or 2

            if user_type == 1:
                date = get_date(i.created)

                result = {
                    "expenditure_numbers" : 1,
                    "expenditure_amounts" : i.amount
                }
                
                db.daily.update({ "user": i.user, 'date': date }, { "$inc": result }, True)

            db.outflow.find_one_and_update({ "_id": i._id }, { "$set": { "statistics": True } })
            counts += 1
            if counts % 1000 == 0:
                print counts
                print time.time() - time1
    except Exception, e:
        import pdb
        pdb.set_trace()
        print e

if __name__ == '__main__':
    while True:
        statistics()
        print '已完成'
        time.sleep(10)