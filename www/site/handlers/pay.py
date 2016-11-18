#!/usr/lib/env python
# -*- encoding:utf-8 -*-

import re
import json
import requests
import datetime
import pymongo
from bson import ObjectId
from urllib import quote
from core.wechat import *
from lixingtie.web import RequestHandler, route
from settings import SERVER_DOMAIN, TRADE_API_URL, MONGODB_HOST, MONGODB_PORT, MONGODB_DB


@route("/pay/wechat/order")
class WechatOrder(RequestHandler):
    def post(self):
        args = json.loads(self.request.body)
        user = args.get("user", "")
        amount = args.get("amount", 0)
        openid = args.get("openid", "")
        
        if not amount:
            return self.json({ "return_code": "ARGUMENT_ERROR", "return_msg": "INVAILD AMOUNT" })
        
        if not openid:
            return self.json({ "return_code": "ARGUMENT_ERROR", "return_msg": "INVAILD OPENID" })
        
        if not user:
            return self.json({ "return_code": "ARGUMENT_ERROR", "return_msg": "INVAILD USER" })

        no = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        client = WeChatPay()
        request = Order()
        request.body = "入金"
        request.detail = "入金"
        request.attach = user
        request.fee_type = "CNY"
        request.total_fee = int(amount) * 100
        request.trade_type = "JSAPI"
        request.notify_url = TRADE_API_URL + "pay/wx/notify"
        request.product_id = no
        request.openid = openid
        request.out_trade_no = no

        client = WeChatPay()
        order = client.order(request)
        
        jsapi_ticket = client.get_jsapi_ticket()

        if order.result_code == "SUCCESS":
            config = JSAPIConfig()
            config.url = SERVER_DOMAIN + "/index.html"
            config.jsapi_ticket = jsapi_ticket.get("ticket")

            prepay_id = order.prepay_id
            request = JSAPIRequest()
            request.package = "prepay_id=" + prepay_id

            result = {}
            result["return_code"] = "SUCCESS"
            result["return_msg"] = "SUCCESS"
            result["config"] = {}
            result["config"]["appId"] = config.appId
            result["config"]["timestamp"] = config.timestamp
            result["config"]["nonceStr"] = config.nonceStr
            result["config"]["signature"] = config.signature

            result["payinfo"] = {}
            result["payinfo"]["timeStamp"] = request.timeStamp
            result["payinfo"]["nonceStr"] = request.nonceStr
            result["payinfo"]["package"] = request.package
            result["payinfo"]["signType"] = request.signType
            result["payinfo"]["paySign"] = request.paySign

            pay = { 
                "no" : no, 
                "type" : 1,
                "user" : ObjectId(user),
                "remark" : "", 
                "fee" : amount,
                "req" : "", 
                "res" : "", 
                "url" : "", 
                "status" : 0,
                "created" : datetime.datetime.now(),
                "args" : { "key" : "" }
            }

            db = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)[MONGODB_DB]
            db.pay.save(pay) 

            return self.json(result)

        return self.json({ "return_code": "ERROR", "return_msg": "ERROR" })
