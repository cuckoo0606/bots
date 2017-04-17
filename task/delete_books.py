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

def delete():
    '''
        在sameorders表里根据orders字段里的_id, 找到books表的args表type为 8和9的记录, 若有重复则删掉
    '''
    orders = db.sameorders.find({ "check": { "$exists": False } })
    for i in orders:
        try:
            # 找到符合要求的books数据
            books = db.books.find({
                "args": { "$in": i.orders },
                "type": { "$in": [8, 9]}
            })
            # 删除相同remark的记录
            same_remark = []
            for b in books:
                print b.remark
                if b.remark not in same_remark:
                    same_remark.append(b.remark)
                else:
                    db.books_bak.save(b)
                    db.books.remove({ "_id": b._id })
                    print 'delete'
            db.sameorders.update({ "_id": i._id }, { "$set": {"check": True} })
            print i.no, 'Done'
        except Exception, e:
            import pdb
            pdb.set_trace()
            print e


if __name__ == '__main__':
    delete()

