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

def new_ratio():
    '''
        1, 数据库删除ratio权限
        2, 数据库添加对应的佣金和红利权限
        3, 管理员添加全部权限
        4, 为避免错误, 手动修改其他角色权限
    '''
    # 删除旧权限
    db.permission.remove({ "code" : "ratio" })
    user = db.permission.find_one({'code' : 'user'})._id
    # 绑定新权限
    com_ratio = ObjectId()
    db.permission.save({"_id": com_ratio, "name": "佣金比例", "parrent": user, "code": "com_ratio"})

    pos_ratio = ObjectId()
    db.permission.save({"_id": pos_ratio, "name": "红利比例", "parrent": user, "code": "pos_ratio"})

    # 管理员添加权限
    admin_role = db.role.find_one({ "roleid" : "admin" })
    admin_per = admin_role.permission
    admin_per.append(str(com_ratio))
    admin_per.append(str(pos_ratio))
    db.role.find_one_and_update({ "roleid" : "admin" }, { "$set" : { "permission" : admin_per } })

if __name__ == '__main__':
    new_ratio()