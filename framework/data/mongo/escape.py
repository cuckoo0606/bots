#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-13


import json
from bson import ObjectId, DBRef
from datetime import datetime
from pymongo.cursor import Cursor
from framework.web.paging import Paging
from framework.data.mongo import Document


class BSONEncoder(json.JSONEncoder):
    """
        BSON序列化JSON编码器
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, DBRef):
            return o.as_doc()

        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%d")
  
        return super(BSONEncoder, self).default(o)
