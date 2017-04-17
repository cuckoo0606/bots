#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../../"))
reload(sys)
sys.setdefaultencoding('utf-8')

from bson import ObjectId
from core.web.handlerbase import find_parents
from framework.data.mongo import db


def figure_commission(user):
    i = 0
    li = []
    users = find_parents(user, [])
    if users:
        try:
            for u in users:
                com = "brokerage" in u and u.brokerage or 0
                if i != 0:
                    bro = com - li[i-1][2]
                else:
                    bro = com
                li.append((u, i, com, bro))
                i += 1
            return True, 1, li
        except Exception, e:
            print e
            return False, -1, "出现异常"
    else:
        return False, 0, "没有符合的上级"


def figure_position(user):
    i = 0
    li = []
    users = find_parents(user, [])
    if users:
        try:
            for u in users:
                pos = "position" in u and u.position or 0
                if i != 0:
                    position = pos - li[i-1][2]
                else:
                    position = pos
                li.append((u, i, pos, position))
                i += 1
            return True, 1, li
        except Exception, e:
            print e
            return False, -1, "出现异常"
    else:
        return False, 0, "没有符合的上级"