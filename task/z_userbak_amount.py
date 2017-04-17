#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef

def user_amount():
    '''
        记录金额变化
    '''
    users = db.user_bak.find()
    for i in users:
        user = db.user.find_one({ "_id": i._id })
        now_amont = round(user.amount, 2)
        db.user_bak.find_one_and_update({ "_id": i._id }, { "$set": { "now_amont": now_amont } })


if __name__ == '__main__':
    user_amount()