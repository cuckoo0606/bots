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

def check_amount():
    '''
        610188  610187   690000  帮忙从后台查询这三个用户下面所有人员在1月1号 和2月10号 的每个人用户的余额和总计
    '''
    o = datetime.timedelta(hours=8)
    starttime = '2017-01-01 00:00:00'
    endtime = '2017-02-10 23:59:59'

    start = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S") - o
    end = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S") - o

    print start
    print end

    user_610188 = db.user.find_one({'userid' : '610188'})
    user_610187 = db.user.find_one({'userid' : '610187'})
    user_690000 = db.user.find_one({'userid' : '690000'})

    print user_610188
    print user_610187
    print user_690000

    # csv
    csv_610188 = csv.writer(open('610188.csv', 'wb'))
    csv_610188.writerow([ '用户'.decode('utf8').encode('gbk'), '开始金额'.decode('utf8').encode('gbk'), '开始时间'.decode('utf8').encode('gbk'), '结束金额'.decode('utf8').encode('gbk'), '结束时间'.decode('utf8').encode('gbk') ])

    # 找出所有下级
    users_610188 = [i._id for i in db.user.find({'relation' : {'$regex' : user_610188.relation}})]
    for i in users_610188:
        user = db.user.find_one({'_id' : i})
        book = [ b for b in db.books.find({'user' : i, 'created' : {'$lt' : start}}).sort([('created', -1)]).limit(1)]
        if not book:
            balance = 0
            created = ""
        else:   
            balance = book[0].balance
            created = (book[0].created - o).strftime("%Y-%m-%d %H:%M:%S")
        
        print '----------------------'
        print user.userid
        print balance
        print created

        book_end = [ b for b in db.books.find({'user' : i, 'created' : {'$lt' : end}}).sort([('created', -1)]).limit(1)]
        if not book_end:
            end_balance = 0
            end_created = ""
        else:
            end_balance = book_end[0].balance
            end_created = (book_end[0].created - o).strftime("%Y-%m-%d %H:%M:%S")
        
        print end_balance
        print end_created
        print '-----------------------'
        csv_610188.writerow([user.userid, round(balance, 2), created, round(end_balance, 2), end_created])

if __name__ == '__main__':
    check_amount()
