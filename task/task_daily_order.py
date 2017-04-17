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
    分用户统计每日资金总表
    编号: userid
    姓名: name
    初始金额: initamount >>
    下单次数: ordernumbers
    盈利次数: profitnumbers
    亏损次数: lossnumbers
    持平次数: flatnumbers
    盈利率: profitability >> 不存数据库
    下单总额: totalamounts
    盈利总额: profitamounts
    亏损总额: lossamounts
    手续费: fees
    佣金次数: commissionnumbers
    佣金总额: commissionamounts
    红利次数: bonusnumbers
    红利总额: bonusamounts
    出金次数: expenditure_numbers
    出金金额: expenditure_amounts
    入金次数: paymentnumbers
    入金总额: paymentamounts

    结构: {userid: userid, date: '2017-02-19', result: {} }

    下单以创建时间为准

    查询是否有空的数据
    db.daily.count({ ordernumbers:{$exists:false},commissionnumbers:{$exists:false},bonusnumbers:{$exists:false},expenditure_numbers:{$exists:false},paymentnumbers:{$exists:false} })
    db.daily.count({ commissionnumbers: {$exists:true} })
    db.daily.count({ bonusnumbers: {$exists:true} })
    db.books.count({"type": {"$in": [8, 9]}, "statistics": {"$exists": true}})
'''

def get_date(created):
    delta = datetime.timedelta(hours=8)
    created = created + delta
    date = created.strftime('%Y-%m-%d')
    result = datetime.datetime.strptime(date + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    return result


def statistics():
    '''
        order: 
        payment
        outflow
    '''
    orders = db.order.find({"statistics": {"$exists": False}, "status" : {"$in" : [110, 120]}})
    counts = 1
    time1 = time.time()
    for i in orders:
        user = db.user.find_one({ "_id": i.user })
        user_type = user and "type" in user and user.type or 2

        if user_type == 1:
            date = get_date(i.created)
            profit = i.profit

            # 初始数据
            profitnumbers = 0
            lossnumbers = 0
            flatnumbers = 0
            profitamounts = 0
            lossamounts = 0
            # 下单次数统计
            if profit > 0:
                profitnumbers = 1
                profitamounts = profit
            elif profit < 0:
                lossnumbers = 1
                lossamounts = profit
            else:
                flatnumbers = 1

            result = {
                "ordernumbers" : 1,
                "totalamounts" : i.money,
                "fees" : i.tax,
                "profitnumbers" : profitnumbers,
                "lossnumbers" : lossnumbers,
                "flatnumbers" : flatnumbers,
                "profitamounts" : profitamounts,
                "lossamounts" : lossamounts
            }
            
            db.daily.update({ "user": i.user, 'date': date }, { "$inc": result }, True)

        db.order.find_one_and_update({ "_id": i._id }, { "$set": { "statistics": True } })
        counts += 1
        if counts % 1000 == 0:
            print counts
            print time.time() - time1

if __name__ == '__main__':
    while True:
        statistics()
        print '已完成'
        time.sleep(10)