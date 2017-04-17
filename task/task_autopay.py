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

try:
    from personal import PAY_TYPE
except:
    PAY_TYPE = ""

if PAY_TYPE == 1:
    from core.logic.bankapply import *

if PAY_TYPE == 2:
    from core.pay.tl import *
    try:
        from personal import TL_APIURL, mchtId, mchtPrivateKeyPassword
    except:
        TL_APIURL = ""
        mchtId = ""
        mchtPrivateKeyPassword = ""

# PAY_TYPE == 3 为开联出金
if PAY_TYPE == 3:
    from core.pay.kl import *
    try:
        from personal import mchtId, notifyUrl, keyFile
    except:
        mchtId = ""
        keyFile = ""
        notifyUrl = ""

'''
    status(1:申请中, 2:已成功, 3:已取消, 4: 处理中, 5: 已失败, 6: 已退款, 7: 出金中, 8: 银行处理中)
    将状态为处理中的订单(状态4)改为已成功(状态2)或已失败(状态5)
    已成功的需要扣除手续费(类型4)
    已失败的需要返钱(类型5)
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
    i = db.outflow.find_one_and_update({ "status" : 4 }, { "$set" : { "status" : 7 } })
    if i:
        try:
            logs = "log" in i and i.log or []
            logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "正在出金!", "operator" : "系统" })
            # 进入处理立即更改状态为7(出金中)
            db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "log" : logs } })
            if "no" in i and "pay_amount" in i:  
                status = -1

                bankholder = i.user_bak.bankholder
                bank = i.user_bak.bank
                bankbranch = i.user_bak.bankbranch
                bankaccount = i.user_bak.bankaccount
                province = i.user_bak.province
                city = i.user_bak.city

                # 汇潮    
                if PAY_TYPE == 1:
                    bankName = "bankName" in i.user_bak and i.user_bak.bankName
                    r = push_info(i.no, bankName, province, city, bankbranch, bankholder, bankaccount, i.pay_amount)
                    
                    if r["resCode"] == "0000":
                        status = 1
                    else:
                        status = -1
                        error_code = "resMessage" in r and r["resMessage"] or "未知错误"

                # 通联
                elif PAY_TYPE == 2:
                    bankName = "bankName" in i.user_bak and i.user_bak.bankName
                    bankNo = "bankNo" in i.user_bak and i.user_bak.bankNo

                    payUrl = "http://221.133.244.5:443/gateway/batch/agentpay"
                    queryUrl = "http://221.133.244.5:443/gateway/batch/agentpayQuery"
                    agent = AgentPay(payUrl, queryUrl, '103000314120004',
                                     '/home/haode/tl_cers/TLCertReal.cer',
                                     '/home/haode/tl_cers/103000314120004.cer',
                                     '/home/haode/tl_cers/103000314120004.pfx', '111111')

                    record = Record(i.no, bankaccount.encode('utf-8'), bankholder.encode('utf-8'), "PERSONAL", bankNo, bankName, int(i.pay_amount*100))
                    
                    request_xml, response_xml = agent.pay("BM-"+i.no, [record])
                    response = xmltodict.parse(response_xml)
                    db.bankpay.insert_one({
                            "no" : i.no,
                            "paytype" : 2,
                            "type" : "pay",
                            "request" : request_xml,
                            "response" : response_xml,
                            "created" : datetime.datetime.now()
                         })

                    if response is not None:
                        body = response['response']['envelope']['body']
                        code = body['info']['responseCode']
                        if code == 'E0000':
                            status = 1
                            records = "records" in body and body["records"] or None
                            if records:
                                e_code = records["record"]["responseCode"]
                                e_msg = records["record"]["responseMsg"]
                                error_code = "{0} : {1}".format(e_code, e_msg)
                                print error_code
                                if e_code == "R1000":
                                    status = 1
                                elif e_code == "R1001":
                                    status = 0
                                else:
                                    status = -1
                        else:
                            status = -1
                            responseMsg = response['response']['envelope']['body']['info']['responseMsg']
                            error_code = "{0} : {1}".format(code, responseMsg)

                 # 开联
                elif PAY_TYPE == 3:
                    bankName = "bankName" in i.user_bak and i.user_bak.bankName

                    payUrl = 'https://pg.openepay.com/gateway/singleagentpay'
                    agent = AgentPay(mchtId, payUrl, notifyUrl, keyFile)
                    record = Record(mchtId, i.no, bankaccount, bankholder, 'PERSONAL', bankId, bankName, int(i.pay_amount*100))
                    pay = agent.pay(record)

                    db.bankpay.insert_one({
                        "no": i.no,
                        "paytype": 3,
                        "type": "pay",
                        "response": pay,
                        "created": datetime.datetime.now()
                    })

                    if pay:
                        code = pay['response']['envelope']['body']['responseCode']
                        responseMsg = pay['response']['envelope']['body']['responseMsg']
                        error_code = "{0} : {1}".format(code, responseMsg)

                        if code == 'E0000':
                            state = pay['response']['envelope']['body']['status']
                            if state == 'TX_BEGIN':
                                status = 0
                            else:
                                status = -1
                        else:
                            status = -1               

                # 已提交成功
                if status == 1:
                    # 出金申请成功, 将处理中状态改为已成功(4改为2)
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "出金申请已成功!", "operator" : "系统" })
                    db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "status" : 2, "log" : logs } })

                    # 2017-3-31更改
                    # 扣除手续费(资金类型4)
                    # handling_charge = "handling_charge" and i.handling_charge or 0
                    # if handling_charge > 0:
                    #     remark = "订单: {0}出金申请已成功, 扣除手续费{1}元.".format(i.no, round(handling_charge, 2))
                    #     books(i.user, 4, handling_charge * -1, {"no" : i._id}, remark)

                # 已提交失败
                elif status == -1:
                    # 出金申请失败, 将处理中状态改为已失败(4改为5), 并记录失败原因
                    desc = "出金已失败, 系统已退款! ({0})".format(error_code)
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : desc, "operator" : "系统" })
                    db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "status" : 5, "log" : logs, "refund" : True } })

                    # 失败订单资金表返现
                    remark = "订单: {0}出金申请已失败, 返还金额{1}元!".format(i.no, round(i.amount, 2))
                    books(i.user, 5, i.amount, {"no" : i._id}, remark)

                # 银行出金中
                elif status == 0:
                    # 银行出金, 将处理中状态改为银行出金中
                    logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "银行处理中", "operator" : "系统" })
                    db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "status" : 8, "log" : logs } })

            else:
                # 没有单号的添加日志, 更改状态
                logs.append({ "addon" : datetime.datetime.utcnow(), "desc" : "订单失败(没有单号或实际出金金额), 系统已退款!", "operator" : "系统" })
                db.outflow.find_one_and_update({ "_id" : i._id }, { "$set" : { "status" : 5, "log" : logs, "refund" : True } })
                remark = "出金申请已失败, 返还金额{0}元.".format(round(i.amount, 2))
                # 失败返款
                books(i.user, 5, i.amount, {"no" : i._id}, remark)
            # print remark
        except Exception, e:
            print e
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    while True:
        job()
        time.sleep(600)
