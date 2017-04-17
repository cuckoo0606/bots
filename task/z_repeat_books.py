#!/usr/lib/env python
# -*- encoding:utf-8 -*-


import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')


import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


def repeat_books():
    bak = db.books_bak.find()
    for i in bak:
        i['repeat'] = True
        db.books.save(i)


if __name__ == '__main__':
    repeat_books()
