#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import random
from bson import ObjectId
from framework.data.mongo import db


def editcode():
    '''
        随机生成6位推荐码
        由数字和小写字母组合
    '''
    str_code = "0123456789abcdefghijklmnopqrstuvwxyz"
    code = "".join([i for i in random.sample(str_code, 6)])
    faildcode = db.user.find_one({"referralcode" : code})
    if faildcode:
        editcode()
    else:
        return code


def usercode():
    '''
        为所有用户生成推荐码
    '''
    users = db.user.find({"type":1, "referralcode" : {"$exists" : False}})
    for i in users:
        i.referralcode = editcode()
        db.user.save(i)
        print "{0} : {1}".format(i.username, i.referralcode)


if __name__ == "__main__":
    usercode()