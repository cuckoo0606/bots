#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import time
import pymongo
import datetime
import requests
import schedule
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


def getIpInfo(ip):
    baidu = "http://ip.taobao.com/service/getIpInfo.php?ip="
    url = baidu + ip
    try:
        r = requests.get(url, timeout=5)
        text = json.loads(r.text)

        if text and text["code"] == 0 and "data" in text and text["data"]:
            data = text["data"]
            country = data["country"]
            region = data["region"]
            city = data["city"]

            st = "%s%s%s" % (country, region, city)
            ipinfo = "%s(%s)" % (ip, st)
        else:
            ipinfo = "%s(未知)" % (ip)
    except Exception, e:
        print e
        ipinfo = "%s(未知)" % (ip)
    return ipinfo

def job():
    try:
        starttime = datetime.datetime(2016,11,11)
        logs = db.systemlog.find({ "status" : {"$exists" : False}, "createtime" : {"$gt" : starttime}})
        print logs.count()
        for i in logs:
            ip = i.ip
            result = "::1" in ip and "::1(本地)" or getIpInfo(ip)
            db.systemlog.find_one_and_update({ "_id" : i._id }, {"$set" : { "ip" : result, "status" : True } })

    except Exception as e:
        print e


if __name__ == "__main__":
    schedule.every(1).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(10)