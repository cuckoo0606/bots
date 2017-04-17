#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-05

import re
import bson
import dateutil.parser


PATTERN_CHINESE = re.compile(r"^[\u4e00-\u9fa5]+$")
PATTERN_EMAIL = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
PATTERN_URL = re.compile(r"^[a-zA-z]+://[^\s]*$")
PATTERN_DIGIT = re.compile(r"^[+-]?\d+(\.\d+)?$")

def ischinese(value):
    """
        字符串是否中文
    """
    return PATTERN_CHINESE.match(value)


def isemail(value):
    """
        字符串是否email地址
    """
    return PATTERN_EMAIL.match(value)


def isdate(value):
    """
        字符串是否日期
    """
    try:
        return dateutil.parser.parse(value)
    except:
        return False


def isurl(value):
    """
        字符串是否url
    """
    return PATTERN_URL.match(value)


def isdigit(value):
    """
        是否有效数字
    """
    return PATTERN_DIGIT.match(value)
