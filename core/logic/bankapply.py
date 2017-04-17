#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
import json
import base64
import hashlib
import datetime
import requests

sys.path.append(os.path.abspath("../../"))
reload(sys)
sys.setdefaultencoding('utf-8')

from bson import ObjectId
from framework.data.mongo import db

try:
    from personal import accountNumber, key, PRODUCE_API, notifyURL, QUREY_API
except:
    accountNumber = ""
    key = ""
    PRODUCE_API = ""
    notifyURL = ""
    QUREY_API = ""

'''
    商户号：""
    KEY：""
    测试地址: https://www.yemadai.com/testtransferapi
    生产地址: https://www.yemadai.com/transferapi
    查询接口: https://api.yemadai.com/queryTransferAPI

    post方式提交transData
'''


def push_info(transId, bankName, provice, city, branchName, accountName, cardNo, \
        amount):
    # 签名
    str_sign = "{0}{1}{2}{3}{4}{5}".format(transId, bankName, accountName, cardNo, amount, key)
    secureCode = hashlib.md5(str_sign).hexdigest().upper()

    # xml主体
    transData = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <yimadai>
            <accountNumber>{0}</accountNumber>
            <notifyURL>{1}</notifyURL>
            <tt>0</tt>
            <transferList>
                <transId>{2}</transId>
                <bankName>{3}</bankName>
                <provice>{4}</provice>
                <city>{5}</city>
                <branchName>{6}</branchName>
                <accountName>{7}</accountName>
                <cardNo>{8}</cardNo>
                <amount>{9}</amount>
                <remark>申请出金</remark>
                <secureCode>{10}</secureCode>
            </transferList>
        </yimadai>""".format(accountNumber, notifyURL, transId, bankName, provice, city, branchName, accountName, cardNo, \
            amount, secureCode)

    # print transData
    base_transData = base64.b64encode(transData)
    # 发送请求
    r = requests.post(PRODUCE_API, data={'transData':base_transData})
    r = json.loads(r.text)

    db.bankpay.insert_one({
            "no" : transId,
            "paytype" : 1,
            "type" : "pay",
            "request" : [transData, base_transData],
            "response" : r,
            "created" : datetime.datetime.now(),
        })

    return r


def query_no(transId, amount):
    # 签名: md5.upper(accountNumber+transId+merchantKey)
    str_sign = "{0}{1}{2}".format(accountNumber, transId, key)
    secureCode = hashlib.md5(str_sign).hexdigest().upper()

    # xml主体
    transData = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
    <yimadai>
        <accountNumber>{0}</accountNumber>
        <transId>{1}</transId>
        <amount>{2}</amount>
        <secureCode>{3}</secureCode>
    </yimadai>""".format(accountNumber, transId, amount, secureCode)

    print transData
    transData = base64.b64encode(transData)
    # 发送请求
    r = requests.post(PRODUCE_API, data={'transData':transData})
    r = json.loads(r.text)
    print r
    return r


if __name__ == "__main__":
    # 单号
    transId = "RA0815143919882848"
    # transId = "R25623154213521"
    # 银行名称, 参照银行列表
    # bankName = "招商银行"
    bankName = '工商'
    # 开户省份
    provice = "广东"
    # 开户城市
    city = "深圳"
    # 支行名称
    branchName = "振华支行"
    # 开户名称
    accountName = "毅"
    # 卡号
    # cardNo = "6214836557502651"
    cardNo = '5226548511122'
    # 金额保留两位小数
    amount = 0.8
    # 备注
    remark = "成功测试"
    query_no(transId, amount)
    # r = push_info(transId, bankName, provice, city, branchName, accountName, cardNo, amount)

'''

'''
