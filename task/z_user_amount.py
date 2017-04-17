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
    users = db.user.find({ 'type': 1 })
    for i in users:
        amount = round(i.amount, 2)

        db.user_bak.insert_one({ '_id': i._id, 'userid': i.userid, 'username': i.username, 'init_amount': amount })


if __name__ == '__main__':
    user_amount()