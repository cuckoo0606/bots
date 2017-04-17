#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')


import csv
import datetime
import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef

def show_infos():
    '''
        截止至2017-2-14的待确认资金流转表
    '''
    o = datetime.timedelta(hours=8)
    starttime = '2017-02-13 00:00:00'
    #endtime = '2017-02-14 23:59:59'

    start = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S") - o
    # end = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S") - o

    outflows = db.outflow.find( {"status": 1, "created" : {"$gt" : start}} )


    # csv
    hengyi_0214 = csv.writer(open('hengyi_0214.csv', 'wb'))
    hengyi_0214.writerow([ '订单号'.decode('utf8').encode('gbk'), '用户id'.decode('utf8').encode('gbk'), '用户名称'.decode('utf8').encode('gbk'), \
        '金额'.decode('utf8').encode('gbk'), '手续费'.decode('utf8').encode('gbk'), '银行'.decode('utf8').encode('gbk'), '支行'.decode('utf8').encode('gbk'), \
        '银行账号'.decode('utf8').encode('gbk'), '开户人'.decode('utf8').encode('gbk'), '省份'.decode('utf8').encode('gbk'), '城市'.decode('utf8').encode('gbk'), \
        '手机号码'.decode('utf8').encode('gbk'), '时间'.decode('utf8').encode('gbk') ])

    kvs = {"CEEBBANK":"中国光大银行", "ABC":"中国农业银行", "BOC":"中国银行", "BOCOM":"交通银行", "CCB":"中国建设银行", "ICBC":"中国工商银行", \
        "PSBC":"中国邮政储蓄银行", "CMBC":"招商银行", "SPDB":"浦发银行", "CEBBANK":"中国光大银行", "ECITIC":"中信银行", "PINGAN":"平安银行", \
        "CMBCS":"中国民生银行", "HXB":"华夏银行", "CGB":"广发银行", "CIB":"兴业银行", "HSB":"徽商银行", "CSCB":"长沙银行", "ZJRCC":"浙江省农村信用社联合社"}

    for i in outflows:
        user = db.user.find_one({ "_id" : i.user })
        print user
        userid = user and "userid" in user and user.userid or ""
        username = user and "username" in user and user.username or ""
        bank = user and "bank" in user and user.bank and kvs[user.bank] or ""
        bankbranch = user and "bankbranch" in user and user.bankbranch or ""
        bankholder = user and "bankholder" in user and user.bankholder or ""
        bankaccount = user and "bankaccount" in user and user.bankaccount or ""
        province = user and "province" in user and user.province or ""
        city = user and "city" in user and user.city or ""
        phone = user and 'phone' in user and user.phone or ""
        amount = "amount" in i and i.amount or 0
        handling_charge = "handling_charge" in i and i.handling_charge or 0
        created = (i.created + o).strftime("%Y-%m-%d %H:%M:%S")

        hengyi_0214.writerow([ i.no, userid, username.decode('utf8').encode('gbk'), amount, handling_charge, bank.decode('utf8').encode('gbk'), \
            bankbranch.decode('utf8').encode('gbk'), "\t"+ bankaccount, bankholder.decode('utf8').encode('gbk'), \
            province.decode('utf8').encode('gbk'), city.decode('utf8').encode('gbk'), "\t"+ phone, created ])


if __name__ == '__main__':
    show_infos()
