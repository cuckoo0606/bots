#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-05

import hashlib


def md5(value):
    hash = hashlib.md5()
    hash.update(value)
    return hash.hexdigest()
