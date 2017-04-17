#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-13


MAP = {
    "yyyy":"%Y",
    "yy":"%y",
    "MM":"%m",
    "dd":"%d",
    "HH":"%H",
    "hh":"%I",
    "mm":"%M",
    "ss":"%S",
    "ddd":"%a",
    "dddd":"%A",
    "MMM":"%b",
    "MMMM":"%B",
    "s":"%c",
    "tt":"%p",
    "t":"%x",
    "T":"%X",
    "zz":"%Z",
}


def pyformat(str_format):
    """
        将一般日期格式化字符串转换为python格式
    """
    keys = MAP.keys()
    keys.sort()
    keys.reverse()
    
    for k in keys:
        str_format = str_format.replace(k, MAP[k])

    return str_format


def general_format(str_format):
    """
        将python格式日期格式化字符串转换为一般格式
    """
    for k, v in __formatmap__.items():
        str_format = str_format.replace(v, k)

    return str_format
