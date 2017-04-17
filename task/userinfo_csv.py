#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import csv
import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef

'''
     导出714个用户
'''

# def export():
#     users = db.user_infos.find({ 'cha': { '$exists': True } })
#     userinfos = csv.writer(open('userinfos.csv', 'wb'))

#     for i in users:
#         userinfos.writerow([ i.userid, i.cha ])

'''
    将现在的用户余额写进去
'''
def write():
    new_userinfos = csv.writer(open('new_userinfos.csv', 'wb'))
    userinfos = csv.reader(file('userinfos.csv', 'rb'))

    for i in userinfos:
        userid, cha = i
        print userid
        print cha
        now_amount = db.user.find_one({ 'userid': userid }).amount
        userinfos.writerow([ userid, cha, now_amount ])

if __name__ == '__main__':
    write()
    # export()