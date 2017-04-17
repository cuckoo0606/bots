#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-05

import os
import bson
import datetime
import dateutil.parser
from bson import ObjectId
import verify


def parse(value, datatype=None):
    """
        从字符串还原数据类型
    """
    if datatype == "str":
        return str(value)
    elif datatype == "int":
        return int(value)
    elif datatype == "objectid":
        return ObjectId(value)
    elif datatype == "float":
        return float(value)
    elif datatype == "bool":
        return bool(value)
    elif datatype == "datetime":
        return dateutil.parser.parse(value)
    elif datatype in ("file", "image"):
        return value
    elif datatype == "object":
        return value
    else:
        if value.lower() == "null" or value.lower() == "none":
            return None

        if value.lower() in ["true", "false"]:
            return value.lower() == "true" and True or False

        try:
            return ObjectId(value)
        except bson.errors.InvalidId:
            pass

        try:
            if verify.isdigit(value):
                return eval(value)
        except:
            pass

        if value in ['a', 'p']:
            return value

        try:
            return dateutil.parser.parse(value)
        except (ValueError, TypeError):
            pass

        return value
