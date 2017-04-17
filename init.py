#!/usr/lib/env python
#-*- encoding:utf-8 -*-

import random
import datetime
from bson import ObjectId
from pymongo import MongoClient
from framework.data.mongo import db, DBRef, Document
from settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_USER, MONGODB_PASSWORD

if __name__ == "__main__":
    # 服务器mongo配置
    # client = MongoClient(MONGODB_HOST, MONGODB_PORT, document_class=Document)[MONGODB_DB]
    # client.authenticate(MONGODB_USER, MONGODB_PASSWORD)

    # db = client

    # 本地mongo配置
    
    db.user.remove()
    db.books.drop()
    db.classify.drop()
    db.commodity.drop()
    db.deposit.drop()
    db.level.drop()
    db.news.drop()
    db.newsclassify.drop()
    db.order.drop()
    db.outflow.drop()
    db.pay.drop()
    db.permission.drop()
    db.recharge.drop()
    db.reminute.drop()
    db.risk.drop()
    db.role.drop()
    db.slipconfig.drop()
    db.systemconfig.drop()
    db.systemlog.drop()
    db.task.drop()
    db.trade.drop()
    db.user.drop()
    db.usergroup.drop()
    db.phonecode.drop()


    '''
        权限设置
    '''
    # 公告管理 news
    # 公告发布 newsis    公告分类 newscl
    news = ObjectId()
    db.permission.save({"_id": news, "name": "公告管理",
                        "parrent": "", "code": "news"})

    newsis = ObjectId()
    db.permission.save({"_id": newsis, "name": "公告发布",
                        "parrent": news, "code": "newsis"})
    newsisa = ObjectId()
    db.permission.save({"_id": newsisa, "name": "添加公告发布",
                        "parrent": newsis, "code": "newsisa"})
    newsisd = ObjectId()
    db.permission.save({"_id": newsisd, "name": "删除公告发布",
                        "parrent": newsis, "code": "newsisd"})
    newsisc = ObjectId()
    db.permission.save({"_id": newsisc, "name": "查询公告发布",
                        "parrent": newsis, "code": "newsisc"})
    newsism = ObjectId()
    db.permission.save({"_id": newsism, "name": "修改公告发布",
                        "parrent": newsis, "code": "newsism"})

    newscl = ObjectId()
    db.permission.save({"_id": newscl, "name": "公告分类",
                        "parrent": news, "code": "newscl"})
    newscla = ObjectId()
    db.permission.save({"_id": newscla, "name": "添加公告分类",
                        "parrent": newscl, "code": "newscla"})
    newscld = ObjectId()
    db.permission.save({"_id": newscld, "name": "删除公告分类",
                        "parrent": newscl, "code": "newscld"})
    newsclc = ObjectId()
    db.permission.save({"_id": newsclc, "name": "查询公告分类",
                        "parrent": newscl, "code": "newsclc"})
    newsclm = ObjectId()
    db.permission.save({"_id": newsclm, "name": "修改公告分类",
                        "parrent": newscl, "code": "newsclm"})

    # 商品管理 commodity
    # 管理商品 commodityma    商品分类 commoditycl      交易模式 commoditytr    损益模式
    # commoditylo
    commodity = ObjectId()
    db.permission.save({"_id": commodity, "name": "商品管理",
                        "parrent": "", "code": "commodity"})

    commodityma = ObjectId()
    db.permission.save({"_id": commodityma, "name": "管理商品",
                        "parrent": commodity, "code": "commodityma"})
    commoditymaa = ObjectId()
    db.permission.save({"_id": commoditymaa, "name": "添加商品",
                        "parrent": commodityma, "code": "commoditymaa"})
    commoditymad = ObjectId()
    db.permission.save({"_id": commoditymad, "name": "删除商品",
                        "parrent": commodityma, "code": "commoditymad"})
    commoditymac = ObjectId()
    db.permission.save({"_id": commoditymac, "name": "查询商品",
                        "parrent": commodityma, "code": "commoditymac"})
    commoditymam = ObjectId()
    db.permission.save({"_id": commoditymam, "name": "修改商品",
                        "parrent": commodityma, "code": "commoditymam"})

    commoditycl = ObjectId()
    db.permission.save({"_id": commoditycl, "name": "商品分类",
                        "parrent": commodity, "code": "commoditycl"})
    commoditycla = ObjectId()
    db.permission.save({"_id": commoditycla, "name": "添加商品分类",
                        "parrent": commoditycl, "code": "commoditycla"})
    commoditycld = ObjectId()
    db.permission.save({"_id": commoditycld, "name": "删除商品分类",
                        "parrent": commoditycl, "code": "commoditycld"})
    commodityclc = ObjectId()
    db.permission.save({"_id": commodityclc, "name": "查询商品分类",
                        "parrent": commoditycl, "code": "commodityclc"})
    commodityclm = ObjectId()
    db.permission.save({"_id": commodityclm, "name": "修改商品分类",
                        "parrent": commoditycl, "code": "commodityclm"})

    commoditytr = ObjectId()
    db.permission.save({"_id": commoditytr, "name": "交易模式",
                        "parrent": commodity, "code": "commoditytr"})
    commoditytra = ObjectId()
    db.permission.save({"_id": commoditytra, "name": "添加交易模式",
                        "parrent": commoditytr, "code": "commoditytra"})
    commoditytrd = ObjectId()
    db.permission.save({"_id": commoditytrd, "name": "删除交易模式",
                        "parrent": commoditytr, "code": "commoditytrd"})
    commoditytrc = ObjectId()
    db.permission.save({"_id": commoditytrc, "name": "查询交易模式",
                        "parrent": commoditytr, "code": "commoditytrc"})
    commoditytrm = ObjectId()
    db.permission.save({"_id": commoditytrm, "name": "修改交易模式",
                        "parrent": commoditytr, "code": "commoditytrm"})

    # 用户 user
    user = ObjectId()
    db.permission.save({"_id": user, "name": "用户管理",
                        "parrent": "", "code": "user"})
    usera = ObjectId()
    db.permission.save({"_id": usera, "name": "添加用户",
                        "parrent": user, "code": "usera"})
    userd = ObjectId()
    db.permission.save({"_id": userd, "name": "删除用户",
                        "parrent": user, "code": "userd"})
    userc = ObjectId()
    db.permission.save({"_id": userc, "name": "查询用户",
                        "parrent": user, "code": "userc"})
    userm = ObjectId()
    db.permission.save({"_id": userm, "name": "修改用户",
                        "parrent": user, "code": "userm"})
    useri = ObjectId()
    db.permission.save({"_id": useri, "name": "用户加款",
                        "parrent": user, "code": "useri"})
    userp = ObjectId()
    db.permission.save({"_id": userp, "name": "用户出金",
                        "parrent": user, "code": "userp"})
    usergroup = ObjectId()
    db.permission.save({"_id": usergroup, "name": "用户组",
                        "parrent": user, "code": "usergroup"})
    level = ObjectId()
    db.permission.save({"_id": level, "name": "用户级别",
                        "parrent": user, "code": "level"})
    status = ObjectId()
    db.permission.save({"_id": status, "name": "状态控制",
                        "parrent": user, "code": "status"})
    com_ratio = ObjectId()
    db.permission.save({"_id": com_ratio, "name": "佣金比例",
                        "parrent": user, "code": "com_ratio"})
    pos_ratio = ObjectId()
    db.permission.save({"_id": pos_ratio, "name": "红利比例",
                        "parrent": user, "code": "pos_ratio"})

    # 权限 permission
    # 角色管理 permissionro    权限管理 permissionpe      角色权限 permissionpr
    permission = ObjectId()
    db.permission.save({"_id": permission, "name": "权限管理",
                        "parrent": "", "code": "permission"})

    permissionro = ObjectId()
    db.permission.save({"_id": permissionro, "name": "角色管理",
                        "parrent": permission, "code": "permissionro"})
    permissionroa = ObjectId()
    db.permission.save({"_id": permissionroa, "name": "添加角色",
                        "parrent": permissionro, "code": "permissionroa"})
    permissionrod = ObjectId()
    db.permission.save({"_id": permissionrod, "name": "删除角色",
                        "parrent": permissionro, "code": "permissionrod"})
    permissionroc = ObjectId()
    db.permission.save({"_id": permissionroc, "name": "查询角色",
                        "parrent": permissionro, "code": "permissionroc"})
    permissionrom = ObjectId()
    db.permission.save({"_id": permissionrom, "name": "修改角色",
                        "parrent": permissionro, "code": "permissionrom"})

    permissionpe = ObjectId()
    db.permission.save({"_id": permissionpe, "name": "权限管理",
                        "parrent": permission, "code": "permissionpe"})
    permissionpea = ObjectId()
    db.permission.save({"_id": permissionpea, "name": "添加权限",
                        "parrent": permissionpe, "code": "permissionpea"})
    permissionped = ObjectId()
    db.permission.save({"_id": permissionped, "name": "删除权限",
                        "parrent": permissionpe, "code": "permissionped"})
    permissionpec = ObjectId()
    db.permission.save({"_id": permissionpec, "name": "查询权限",
                        "parrent": permissionpe, "code": "permissionpec"})
    permissionpem = ObjectId()
    db.permission.save({"_id": permissionpem, "name": "修改权限",
                        "parrent": permissionpe, "code": "permissionpem"})

    permissionpr = ObjectId()
    db.permission.save({"_id": permissionpr, "name": "角色权限",
                        "parrent": permission, "code": "permissionpr"})
    permissionpra = ObjectId()
    db.permission.save({"_id": permissionpra, "name": "添加角色权限",
                        "parrent": permissionpr, "code": "permissionpra"})
    permissionprd = ObjectId()
    db.permission.save({"_id": permissionprd, "name": "删除角色权限",
                        "parrent": permissionpr, "code": "permissionprd"})
    permissionprc = ObjectId()
    db.permission.save({"_id": permissionprc, "name": "查询角色权限",
                        "parrent": permissionpr, "code": "permissionprc"})
    permissionprm = ObjectId()
    db.permission.save({"_id": permissionprm, "name": "修改角色权限",
                        "parrent": permissionpr, "code": "permissionprm"})

    # 资金流转 fundsflow
    fundsflow = ObjectId()
    db.permission.save({"_id": fundsflow, "name": "资金流转",
                        "parrent": "", "code": "fundsflow"})

    pay = ObjectId()
    db.permission.save(
        {"_id": pay, "name": "出金", "parrent": fundsflow, "code": "pay"})
    income = ObjectId()
    db.permission.save({"_id": income, "name": "入金",
                        "parrent": fundsflow, "code": "income"})
    payreport = ObjectId()
    db.permission.save({"_id": payreport, "name": "出金纪录",
                        "parrent": fundsflow, "code": "payreport"})
    incomereport = ObjectId()
    db.permission.save({"_id": incomereport, "name": "入金纪录",
                        "parrent": fundsflow, "code": "incomereport"})
    confirm = ObjectId()
    db.permission.save({"_id": confirm, "name": "资金确认",
                        "parrent": fundsflow, "code": "confirm"})

    # 订单管理 oder
    oder = ObjectId()
    db.permission.save({"_id": oder, "name": "订单管理",
                        "parrent": "", "code": "oder"})

    oderwa = ObjectId()
    db.permission.save({"_id": oderwa, "name": "持仓单查询",
                        "parrent": oder, "code": "oderwa"})
    oderhi = ObjectId()
    db.permission.save({"_id": oderhi, "name": "历史订单查询",
                        "parrent": oder, "code": "oderhi"})

    # 风险管理 risk
    risk = ObjectId()
    db.permission.save({"_id": risk, "name": "风险管理",
                        "parrent": "", "code": "risk"})

    riskmanage = ObjectId()
    db.permission.save({"_id": riskmanage, "name": "风险编辑",
                        "parrent": risk, "code": "riskmanage"})

    riskmanagea = ObjectId()
    db.permission.save({"_id": riskmanagea, "name": "添加风险",
                        "parrent": riskmanage, "code": "riskmanagea"})
    riskmanaged = ObjectId()
    db.permission.save({"_id": riskmanaged, "name": "删除风险",
                        "parrent": riskmanage, "code": "riskmanaged"})
    riskmanagec = ObjectId()
    db.permission.save({"_id": riskmanagec, "name": "查询风险",
                        "parrent": riskmanage, "code": "riskmanagec"})
    riskmanagem = ObjectId()
    db.permission.save({"_id": riskmanagem, "name": "修改风险",
                        "parrent": riskmanage, "code": "riskmanagem"})

    riskkey = ObjectId()
    db.permission.save({"_id": riskkey, "name": "重点客户",
                        "parrent": risk, "code": "riskkey"})

    # 报表管理 report
    report = ObjectId()
    db.permission.save({"_id": report, "name": "报表管理",
                        "parrent": "", "code": "report"})

    commission = ObjectId()
    db.permission.save({"_id": commission, "name": "佣金报表",
                        "parrent": report, "code": "commission"})
    position = ObjectId()
    db.permission.save({"_id": position, "name": "红利报表",
                        "parrent": report, "code": "position"})
    booksreport = ObjectId()
    db.permission.save({"_id": booksreport, "name": "资金报表",
                        "parrent": report, "code": "booksreport"})
    personal = ObjectId()
    db.permission.save({"_id": personal, "name": "个人报表",
                        "parrent": report, "code": "personal"})

    # 系统管理
    system = ObjectId()
    db.permission.save({"_id": system, "name": "系统管理",
                    "parrent": "", "code": "system"})

    systemconfig = ObjectId()
    db.permission.save({"_id": systemconfig, "name": "系统设置",
                        "parrent": system, "code": "systemconfig"})
    systemlog = ObjectId()
    db.permission.save({"_id": systemlog, "name": "系统日志",
                        "parrent": system, "code": "systemlog"})

    '''
        管理员权限
    '''
    created = datetime.datetime.now()
    pers = db.permission.find()
    per = []
    for i in pers:
        try:
            per.append(str(i["_id"]))
        except Exception, e:
            import pdb; pdb.set_trace()
            print i

    role_admin_id = ObjectId()
    db.role.save({"_id": role_admin_id, "rolename": "管理员",
                  "roleid": "admin", "permission": per})

    str_code = "0123456789abcdefghijklmnopqrstuvwxyz"
    admin_id = ObjectId()

    '''
        管理员初始化
    '''
    code_admin = "".join([i for i in random.sample(str_code, 6)])

    u = {}
    u["_id"] = admin_id
    u["userid"] = "admin"
    u["username"] = "管理员"
    u["password"] = "21232f297a57a5a743894a0e4a801fc3"
    u["IDcard"] = "440887199609081133"
    u["accountholder"] = "华盛顿"
    u["email"] = "47598@qq.com"
    u["address"] = "广州"
    u["sex"] = "male"
    u["phone"] = "13877665788"
    u["amount"] = 0
    u["parent"] = ""
    u["type"] = 1
    u["amount"] = 9999999
    u["relation"] = "/admin"
    u["userrole"] = DBRef("role", role_admin_id)
    u["created"] = datetime.datetime.now()
    u["referralcode"] = code_admin
    u["status"] = 1

    db.user.save(u)

    role_agent_id = ObjectId()
    agent_per = [str(i) for i in (commodity, commodityma, commoditymac, commoditytr, commoditytra, commoditytrc, \
                                  user, usera, userd, userc, userm, useri, userp, permissionpr, permissionprm, fundsflow, pay, \
                                  income, payreport, incomereport, oder, oderwa, oderhi, risk, riskmanagea,\
                                  riskmanaged, riskmanagec, riskmanagem, riskkey, report, commission, \
                                  position, system, systemconfig, systemlog)]
    '''
        代理商初始化
    '''
    db.role.save({"_id": role_agent_id, "rolename": "代理商",
                  "roleid": "agent", "permission": agent_per})

    code = "".join([i for i in random.sample(str_code, 6)])

    agent_id = ObjectId()

    agent = {}
    agent["_id"] = agent_id
    agent["userid"] = "agent"
    agent["username"] = "代理商"
    agent["password"] = "21232f297a57a5a743894a0e4a801fc3"
    agent["IDcard"] = ""
    agent["accountholder"] = ""
    agent["email"] = ""
    agent["address"] = ""
    agent["sex"] = "male"
    agent["phone"] = ""
    agent["amount"] = 0
    agent["type"] = 1
    agent["parent"] = DBRef("user", admin_id)
    agent["relation"] = "/admin/" + str(agent_id)
    agent["userrole"] = DBRef("role", role_agent_id)
    agent["created"] = datetime.datetime.now()
    agent["referralcode"] = code
    u["status"] = 1

    db.user.save(agent)

    role_member_id = ObjectId()
    member_per = [str(i) for i in (commodity, commoditymac, commoditytr, commoditytrc, user,
                                   oder, oderwa, oderhi, fundsflow, pay, income, payreport, incomereport
                                   )]
    '''
        会员权限
    '''
    db.role.save({"_id": role_member_id, "rolename": "会员",
                  "roleid": "member", "permission": member_per})

    '''
        商品类型初始化
    '''
    # 指数
    index = ObjectId()
    # 外汇
    IB = ObjectId()
    # 商品
    SP = ObjectId()

    db.classify.save({"_id" : index, "code" : "index", "name" : "指数"})
    db.classify.save({"_id" : IB, "code" : "IB", "name" : "外汇"})
    db.classify.save({"_id" : SP, "code" : "SP", "name" : "商品"})

    '''
        商品初始化
    '''

    # 恒生指数(HKIF HSI 1609) >> 指数
    HKIF_HSI_1609 = ObjectId()
    db.commodity.save({ "_id" : HKIF_HSI_1609, "code" : "HKIF HSI 1609", "name" : "恒生指数",\
        "created" : created, "decimal" : 0, "isgroup" : "1", "intro" : "恒生指数", "openingday" : 0,\
        "classify" : DBRef("classify", index), "openingtime" : "09:12-11:30,14:30-15:30,17:30-23:00",\
        "market" : "HKIF", "quotation" : "恒生指数" })

    # 原油(NYMEX_CL_1609) >> 商品
    NYMEX_CL_1609 = ObjectId()
    db.commodity.save({ "_id" : NYMEX_CL_1609, "code" : "NYMEX CL 1609", "name" : "原油",\
        "created" : created, "decimal" : 2, "isgroup" : "1", "intro" : "原油", "openingday" : 0,\
        "classify" : DBRef("classify", SP), "openingtime" : "00:00-23:59",\
        "market" : "NYMEX", "quotation" : "原油", "created" : created })

    # 美元/加元(USD_CAD) >> 外汇
    USD_CAD = ObjectId()
    db.commodity.save({ "_id" : USD_CAD, "code" : "USD.CAD", "intro" : "USD.CAD", "openingday" : 0,\
        "market" : "IB", "quotation" : "USD.CAD", "name" : "美元/加元", "decimal" : 5, "isgroup" : "1",\
        "openingtime" : "00:00-23:59", "classify" : DBRef("classify", IB), "created" : created })

    # 欧元/美元(EUR_USD) >> 外汇
    EUR_USD = ObjectId()
    db.commodity.save({ "_id" : EUR_USD, "code" : "EUR.USD", "intro" : "EUR.USD", "openingday" : 0,\
        "market" : "IB", "quotation" : "EUR.USD", "name" : "欧元/美元", "decimal" : 4, "isgroup" : "1",\
        "openingtime" : "00:00-23:59", "classify" : DBRef("classify", IB), "created" : created })

    # 美元/日元(USD_JPY) >> 外汇
    USD_JPY = ObjectId()
    db.commodity.save({ "_id" : USD_JPY, "code" : "USD.JPY", "intro" : "USD.JPY", "openingday" : 0,\
        "market" : "IB", "quotation" : "USD.JPY", "name" : "美元/日元", "decimal" : 4, "isgroup" : "1",\
        "openingtime" : "00:00-23:59", "classify" : DBRef("classify", IB), "created" : created })

    # 英镑/美元(GBP_USD) >> 外汇
    GBP_USD = ObjectId()
    db.commodity.save({ "_id" : GBP_USD, "code" : "GBP.USD", "intro" : "GBP.USD", "openingday" : 0,\
        "market" : "IB", "quotation" : "GBP.USD", "name" : "英镑/美元", "decimal" : 4, "isgroup" : "1",\
        "openingtime" : "00:00-23:59", "classify" : DBRef("classify", IB), "created" : created })

    # 澳元/美元(AUD_USD) >> 外汇
    AUD_USD = ObjectId()
    db.commodity.save({ "_id" : AUD_USD, "code" : "AUD.USD", "intro" : "AUD.USD", "openingday" : 0,\
        "market" : "IB", "quotation" : "AUD.USD", "name" : "澳元/美元", "decimal" : 4, "isgroup" : "1",\
        "openingtime" : "00:00-23:59", "classify" : DBRef("classify", IB), "created" : created })

    # 英镑/日元(GBP_JPY) >> 外汇
    GBP_JPY = ObjectId()
    db.commodity.save({ "_id" : GBP_JPY, "code" : "GBP.JPY", "intro" : "GBP.JPY", "openingday" : 0,\
        "market" : "IB", "quotation" : "GBP.JPY", "name" : "英镑/日元", "decimal" : 2, "isgroup" : "1",\
        "openingtime" : "00:00-23:59", "classify" : DBRef("classify", IB), "created" : created })

    # 澳元/日元(AUD_JPY) >> 外汇
    AUD_JPY = ObjectId()
    db.commodity.save({ "_id" : AUD_JPY, "code" : "AUD.JPY", "intro" : "AUD.JPY", "openingday" : 0,\
        "market" : "IB", "quotation" : "AUD.JPY", "name" : "澳元/日元", "decimal" : 4, "isgroup" : "1",\
        "openingtime" : "", "classify" : DBRef("classify", IB), "created" : created })

    # 纽元/日元(NZD_JPY) >> 指数
    NZD_JPY = ObjectId()
    db.commodity.save({ "_id" : NZD_JPY, "code" : "NZD.JPY", "intro" : "纽元/日元", "openingday" : 0,\
        "market" : "IB", "quotation" : "NZD.JPY", "name" : "纽元/日元", "decimal" : 4, "isgroup" : "1",\
        "openingtime" : "", "classify" : DBRef("classify", index), "created" : created })

    # 欧元/日元(EUR_JPY) >> 指数
    EUR_JPY = ObjectId()
    db.commodity.save({ "_id" : EUR_JPY, "code" : "EUR.JPY", "intro" : "欧元/日元", "openingday" : 0,\
        "market" : "IB", "quotation" : "EUR.JPY", "name" : "欧元/日元", "decimal" : 4, "isgroup" : "1",\
        "openingtime" : "", "classify" : DBRef("classify", index), "created" : created })

    # 美原油(USO_IL) >> 商品
    USO_IL = ObjectId()
    db.commodity.save({ "_id" : USO_IL, "code" : "USO.IL", "name" : "美原油", "created" : created,\
        "decimal" : 2, "isgroup" : "1", "intro" : "美原油", "openingday" : 0,\
        "classify" : DBRef("classify", SP), "openingtime" : "", "market" : "IB", "quotation" : "USO.IL" })

    # 新华富时A50(SGX_CN_1609) >> 指数
    SGX_CN_1609 = ObjectId()
    db.commodity.save({ "_id" : SGX_CN_1609, "code" : "SGX CN 1609", "name" : "新华富时A50", "created" : created,\
        "decimal" : 0, "isgroup" : "1", "intro" : "新华富时A50", "openingday" : 0, "classify" : DBRef("classify", index),\
        "openingtime" : "09:00-12:00,13:00-16:00,16:30-23:45", "market" : "SGX", "quotation" : "SGX CN 1609" })


    '''
        交易模式初始化
    '''
    # 恒生指数 短期/长期/60秒
    db.trade.save({ "status" : 1, "assets" : str(HKIF_HSI_1609), "commodity" : DBRef("commodity", HKIF_HSI_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:15" },\
            { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:30" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:45" },\
            { "outprice" : 0.05, "inprice" : 0.8, "time" : "13:00" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "23:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(HKIF_HSI_1609), "commodity" : DBRef("commodity", HKIF_HSI_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.85, "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(HKIF_HSI_1609), "commodity" : DBRef("commodity", HKIF_HSI_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0.05, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0.05, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0.05, "inprice" : 0.75, "time" : "240" } ] })

    # 原油 短期/长期/60秒
    db.trade.save({ "status" : 1, "assets" : str(NYMEX_CL_1609), "commodity" : DBRef("commodity", NYMEX_CL_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:15" },\
        { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:30" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:45" },\
        { "outprice" : 0.05, "inprice" : 0.8, "time" : "13:00" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "23:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(NYMEX_CL_1609), "commodity" : DBRef("commodity", NYMEX_CL_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.85, "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(NYMEX_CL_1609), "commodity" : DBRef("commodity", NYMEX_CL_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0.05, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0.05, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0.05, "inprice" : 0.75, "time" : "240" } ] })

    # 美元/加元 短期/长期/60秒
    db.trade.save({ "status" : 1, "assets" : str(USD_CAD), "commodity" : DBRef("commodity", USD_CAD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:15" },\
        { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:30" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "12:45" },\
        { "outprice" : 0.05, "inprice" : 0.8, "time" : "13:00" }, { "outprice" : 0.05, "inprice" : 0.8, "time" : "23:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(USD_CAD), "commodity" : DBRef("commodity", USD_CAD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.85, "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(USD_CAD), "commodity" : DBRef("commodity", USD_CAD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0.05, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0.05, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0.05, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0.05, "inprice" : 0.75, "time" : "240" } ] })

    # 欧元/美元 短期/长期/60秒
    db.trade.save({ "status" : 1, "assets" : str(EUR_USD), "commodity" : DBRef("commodity", EUR_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(EUR_USD), "commodity" : DBRef("commodity", EUR_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.85, "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(EUR_USD), "commodity" : DBRef("commodity", EUR_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 美元/日元 短期/长期/60秒
    db.trade.save({ "status" : 1, "assets" : str(USD_JPY), "commodity" : DBRef("commodity", USD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(USD_JPY), "commodity" : DBRef("commodity", USD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.85, "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(USD_JPY), "commodity" : DBRef("commodity", USD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 英镑/美元
    db.trade.save({ "status" : 1, "assets" : str(GBP_USD), "commodity" : DBRef("commodity", GBP_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(GBP_USD), "commodity" : DBRef("commodity", GBP_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.85,  "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(GBP_USD), "commodity" : DBRef("commodity", GBP_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 澳元/美元
    db.trade.save({ "status" : 1, "assets" : str(AUD_USD), "commodity" : DBRef("commodity", AUD_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(AUD_USD), "commodity" : DBRef("commodity", AUD_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.85, "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(AUD_USD), "commodity" : DBRef("commodity", AUD_USD),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 英镑/日元
    db.trade.save({ "status" : 1, "assets" : str(GBP_JPY), "commodity" : DBRef("commodity", GBP_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(GBP_JPY), "commodity" : DBRef("commodity", GBP_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [  {  "outprice" : 0,  "inprice" : 0.85,  "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(GBP_JPY), "commodity" : DBRef("commodity", GBP_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 澳元/日元
    db.trade.save({ "status" : 1, "assets" : str(AUD_JPY), "commodity" : DBRef("commodity", AUD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(AUD_JPY), "commodity" : DBRef("commodity", AUD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 1, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.85, "time" : "28-12:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(AUD_JPY), "commodity" : DBRef("commodity", AUD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 纽元/日元
    db.trade.save({ "status" : 1, "assets" : str(NZD_JPY), "commodity" : DBRef("commodity", NZD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(NZD_JPY), "commodity" : DBRef("commodity", NZD_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 欧元/日元
    db.trade.save({ "status" : 1, "assets" : str(EUR_JPY), "commodity" : DBRef("commodity", EUR_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(EUR_JPY), "commodity" : DBRef("commodity", EUR_JPY),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "60" }, { "outprice" : 0, "inprice" : 0.75, "time" : "120" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "180" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 美原油
    db.trade.save({ "status" : 1, "assets" : str(USO_IL), "commodity" : DBRef("commodity", USO_IL),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(USO_IL), "commodity" : DBRef("commodity", USO_IL),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "60" }, { "outprice" : 0, "inprice" : 0.75, "time" : "120" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "180" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    # 新华富时A50
    db.trade.save({ "status" : 1, "assets" : str(SGX_CN_1609), "commodity" : DBRef("commodity", SGX_CN_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 0, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.8, "time" : "12:00" }, { "outprice" : 0, "inprice" : 0.8, "time" : "16:00" },\
        { "outprice" : 0, "inprice" : 0.8, "time" : "20:00" } ] })

    db.trade.save({ "status" : 1, "assets" : str(SGX_CN_1609), "commodity" : DBRef("commodity", SGX_CN_1609),\
        "amounts" : [ 100, 200, 500, 1000, 2000, 5000 ], "mode" : 2, "createtime" : created,\
        "cycle" : [ { "outprice" : 0, "inprice" : 0.75, "time" : "30" }, { "outprice" : 0, "inprice" : 0.75, "time" : "60" },\
        { "outprice" : 0, "inprice" : 0.75, "time" : "120" }, { "outprice" : 0, "inprice" : 0.75, "time" : "240" } ] })

    '''
        系统设置初始化
    '''
    db.systemconfig.save({ "value" : 10000, "key" : "sim-initial-amount" })
    db.systemconfig.save({ "value" : 10000, "key" : "warning-total-amount" })
    db.systemconfig.save({ "value" : 100, "key" : "warning-single-amount" })
    db.systemconfig.save({ "value" : 5, "key" : "oneminute-trading-count" })
    db.systemconfig.save({ "value" : 30000, "key" : "oneminute-trading-amount" })
    db.systemconfig.save({ "value" : "1:2", "key" : "risk-pupil-ratio" })
    db.systemconfig.save({ "value" : 300, "key" : "risk-trading-amount" })
    db.systemconfig.save({ "__v" : 0, "key" : "risk-auto-run", "value" : "true" })
    db.systemconfig.save({ "__v" : 0, "key" : "risk-auto-points", "value" : "1" })
    db.systemconfig.save({ "__v" : 0, "key" : "risk-auto-min", "value" : "5000" })
    db.systemconfig.save({ "value" : "09:00", "key" : "pay-starttime" })
    db.systemconfig.save({ "value" : "22:00", "key" : "pay-endtime" })
    db.systemconfig.save({ "value" : 10, "key" : "pay-handling-charge" })
    db.systemconfig.save({ "value" : 1000, "key" : "pay-quota-amount" })
    db.systemconfig.save({ "value" : "09:00", "key" : "income-starttime" })
    db.systemconfig.save({ "value" : "22:00", "key" : "income-endtime" })
    db.systemconfig.save({ "value" : 5, "key" : "income-handling-charge" })
    db.systemconfig.save({ "value" : 1000, "key" : "income-quota-amount" })
    db.systemconfig.save({ "value" : "0", "key" : "pay-handling-type" })
