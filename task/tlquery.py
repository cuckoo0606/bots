#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
import time
import pymongo
import datetime

sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

from bson import ObjectId
from framework.data.mongo import db, Document, DBRef

from core.pay.tl import *
try:
    from personal import TL_APIURL, mchtId, mchtPrivateKeyPassword
except:
    TL_APIURL = ""
    mchtId = ""
    mchtPrivateKeyPassword = ""


'''
    status(1:申请中, 2:已成功, 3:已取消, 4: 处理中, 5: 已失败, 6: 已退款, 7: 出金中, 8: 银行处理中)
    查询状态为银行处理中的订单, 并将查询到的状态更改或维持不变
    如果成功则扣除手续费
'''


def books(user, bookstype, amount, args, remark):
    result = db.user.find_one_and_update({"_id" : user}, {"$inc" : {"amount" : amount}}, return_document=pymongo.ReturnDocument.AFTER)

    # 增加资金流转记录
    books = {
        "user" : user,
        "amount" : amount,
        "balance" : result.amount,
        "type" : bookstype,
        "args" : args,
        "remark" : remark,
        "created" : datetime.datetime.utcnow()
    }
    db.books.insert_one(books)


def job():
    print "start work!"
    rs = db.outflow.find({ "status" : 8 })
    for i in rs:
        try:
            logs = "log" in i and i.log or []

            payUrl = "http://221.133.244.5:443/gateway/batch/agentpay"
            queryUrl = "http://221.133.244.5:443/gateway/batch/agentpayQuery"
            agent = AgentPay(payUrl, queryUrl, '103000314120004',
                             '/home/haode/tl_cers/TLCertReal.cer',
                             '/home/haode/tl_cers/103000314120004.cer',
                             '/home/haode/tl_cers/103000314120004.pfx', '111111')

            request_xml, response_xml = agent.query("BM-"+i.no)
            print request_xml
            print response_xml
            response = xmltodict.parse(response_xml)

            e_code = response['response']['envelope']['body']['info']['responseCode']

            db.bankpay.insert_one({
                "no" : i.no,
                "paytype" : 2,
                "type" : "query",
                "request" : request_xml,
                "response" : response_xml,
                "created" : datetime.datetime.now()
             })

            if e_code == "E0000":
                code = response['response']['envelope']['body']['records']['record']['status']
                if code == u'代付处理完成':
                    print "成功"
                    # 出金申请成功, 将处理中状态改为已成功(4改为2)
                    desc = "出金申请已成功!({0})".format(code)
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : desc, "operator" : "系统" })
                    db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "status" : 2, "log" : logs } })

                    # 扣除手续费(资金类型4)
                    handling_charge = "handling_charge" and i.handling_charge or 0
                    if handling_charge > 0:
                        remark = "订单: {0}出金申请已成功, 扣除手续费{1}元.".format(i.no, round(handling_charge, 2))
                        books(i.user, 4, handling_charge * -1, {"no" : i._id}, remark)
                elif code == u'代付处理失败':
                    print "失败"
                    # 出金申请失败, 将处理中状态改为已失败(4改为5), 并记录失败原因
                    desc = "出金已失败, 系统已退款! ({0})".format(code)
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : desc, "operator" : "系统" })
                    db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "status" : 5, "log" : logs, "refund" : True } })

                    # 失败订单资金表返现
                    remark = "订单: {0}出金申请已失败, 返还金额{1}元!".format(i.no, round(i.amount, 2))
                    books(i.user, 5, i.amount, {"no" : i._id}, remark)
                else:
                    desc = "正在处理中! ({0})".format(code)
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : desc, "operator" : "系统" })
                    db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "log" : logs } })
            else:
                msg = response['response']['envelope']['body']['info']['responseMsg']
                desc = "查询失败! ({0} : {1})".format(e_code, msg)
                logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : desc, "operator" : "系统" })
                db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "log" : logs } })

        except Exception, e:
            print e

if __name__ == "__main__":
    while True:
        job()
        time.sleep(1800)
