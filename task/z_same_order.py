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

def check_orders(starttime, endtime):
    '''
        计算出相同订单的订单号和重复数量
    '''
    select_time = {}
    select_time["$gte"] = datetime.datetime.strptime(starttime, "%Y-%m-%d  %H:%M:%S.%f")
    select_time["$lt"] = datetime.datetime.strptime(endtime, "%Y-%m-%d  %H:%M:%S.%f")

    orders = db.order.aggregate(
        [
            {"$match":{
                "status":110,
                "created":select_time
                }
            },
            {"$group":{
                '_id': "$no",
                "count":{
                    "$sum":1}
                    }
                },
            {"$match":{
                "count":{"$gt":1}
                }
            }
        ]
    )

    n = 0
    for i in orders:
        print i
        n = n+1
        db.sameorders.insert_one({ "no": i._id, "count": i.count })
    print n

if __name__ == '__main__':
    starttime = '2016-06-01 16:00:00.000'
    endtime = '2017-01-01 16:00:00.000'
    check_orders(starttime, endtime)
