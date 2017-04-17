#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
import pymongo
import datetime
from bson import ObjectId
from core.web.handlerbase import find_parents
from framework.data.mongo import db, Document, DBRef


orders = db.order.find({"status" : {"$in" : [110, 120]}, "score" : {"$exists" : False}})
print orders.count()
try:
    for i in orders:
        if "profit" in i:
            if i.profit > 0:
                i.score = 1
            elif i.profit == 0:
                i.score = 0
            elif i.profit < 0:
                i.score = -1

            db.order.save(i)
except Exception, e:
    print e
    import pdb; pdb.set_trace()