#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import arrow
import time
import schedule
from framework.data.mongo import db, Document, DBRef


'''
    每天21时计算一次余额少于500的符合要求的代理商
    代理商要求: 有红利设置, 余额少于500, 角色为agent
'''
agent_roleid = db.role.find_one({ 'roleid': 'agent' })._id

def job():
    print 'Start working'
    now = arrow.now()
    date = "{0}-{1}-{2}".format(now.year, now.month, now.day)

    where = {}
    where['userrole.$id'] = agent_roleid
    where['position'] = {'$exists': True}
    where['amount'] = {'$lt': 500}

    users = db.user.find(where)
    li = []
    for i in users:
        result={}
        result['userid'] = i.userid
        result['username'] = i.username
        result['amount'] = i.amount != 0 and round(i.amount, 2) or 0
        result['date'] = date
         
        db.warning_user.insert_one(result)
    print 'Ending work'

if __name__ == "__main__":
    schedule.every().day.at('17:53').do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)