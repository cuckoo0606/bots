#!/usr/lib/env python
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


def export():
    doc = csv.writer(open('user_amount.csv', 'wb'))
    users = db.user_bak.find({ 'cha' : {'$nin': [0]} })

    print users.count()
    for i in users:
        doc.writerow([ "\t"+i.userid, i.init_amount, i.now_amont, i.cha ])


if __name__ == '__main__':
    export()
