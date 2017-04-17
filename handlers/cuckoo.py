#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25


def per_result(per, UP):
    """
        输出当前页面权限结果
    """
    result = False
    for i in per:
        if i in UP:
            result = True
            break

    return result