#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')


import pymongo
import datetime
import schedule
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef



def test():
    orders = db.order.aggregate(
        [
            {"$match":{"status":110}},
            {"$group":
                {
                    "_id":'$no',
                    "count":{"$sum":1}
                }
            },
            {"$match":{"count":{"$gt":1}}}
        ]
    )
    for i in orders:
        same_orders = db.order.find({ "no": i._id })
        for s in same_orders:
            user = db.user.find_one({ "_id": s.user })
            user_type = "type" in user and user.type or "空类型"
            user_relation = "relation" in user and user.relation or "空关系"

            print '订单号: {0}'.format(i._id)
            print '订单id: {0}'.format(str(s._id))
            print '用户id: {0}'.format(user.userid)
            print '用户类型: {0}'.format(user_type)
            print '用户关系: {0}'.format(user_relation)



if __name__ == '__main__':
    test()


'''
    db.order.update({no:'R20170207095954695'}, {$unset:{profit_process:1}},{multi:1})
'''