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
    手续费: Fees
    佣金: commission
    红利: bonus
    出金申请: 
    出金失败:
    出金次数
    入金次数: paymentnumbers
    入金总额: paymentamounts

    下单以创建时间为准
'''

def get_date(created):
    '''
        时间戳 create_time
        时间戳转换为北京时间的日期的datetime
    '''
    timeStamp = created / 1000
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    result = datetime.datetime.strptime(otherStyleTime + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    return result


def statistics():
    '''
        payment: 入金总额和次数
    '''
    payments = db.payment.find({ "status": 2, "statistics": {"$exists": False} })
    print payments.count()
    counts = 1
    time1 = time.time()
    for i in payments:
        user = db.user.find_one({ "_id": i.user_id })
        user_type = user and "type" in user and user.type or 2

        if user_type == 1:
            date = get_date(i.create_time)

            result = {
                "paymentnumbers" : 1,
                "paymentamounts" : i.fee
            }
            
            db.daily.update({ "user": i.user_id, 'date': date }, { "$inc": result }, True)

        db.payment.find_one_and_update({ "_id": i._id }, { "$set": { "statistics": True } })
        counts += 1
        if counts % 1000 == 0:
            print counts
            print time.time() - time1

if __name__ == '__main__':
    while True:
        statistics()
        print '已完成'
        time.sleep(60)