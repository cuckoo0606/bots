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

def add_ratio():
    '''
        添加比例设置权限, 在用户权限下
    '''
    if not db.permission.find_one({"code" : "ratio"}):
        per_user_id = db.permission.find_one({"code" : "user"})._id
        db.permission.save({
            "code" : "ratio",
            "name" : "比例设置",
            "parrent" : per_user_id
        })

    pers = db.permission.find()
    per = []
    for i in pers:
        try:
            per.append(str(i["_id"]))
        except Exception, e:
            print i

    role_admin_id = db.role.find_one({"roleid" : "admin"})._id
    db.role.update({"_id": role_admin_id}, {"$set" : {"permission" : per}})

add_ratio()