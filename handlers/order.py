#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25
import re
import os
import tornado.web
import datetime
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.data.mongo import db, Document
from bson import ObjectId

# ELA
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')
from settings import DEFAULT_PAGESIZE

@url("/order/warehouseinpuire")
class WarehouseInpuire(HandlerBase):

    @tornado.web.authenticated
    def statistics_ware(self, where):
        try:
            ware = db.order.aggregate([
                {
                    "$match" : where
                },
                {
                    "$group" : {    
                        "_id" : -1,
                        "count" : { "$sum" : 1 },
                        "money" : { "$sum" : "$money" },
                        "tax" : { "$sum" : "$tax" }
                    }
                }
            ])
            ware = ware and list(ware) or []
            return ware
        except Exception, e:
            print e
            return []

    @tornado.web.authenticated
    def get(self):
        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        mode = self.get_argument("mode", "-1")
        receiver = self.get_argument("receiver", "")
        subordinate = self.get_argument("subordinate", "")
        direction = self.get_argument("direction", "-1")
        statistics = self.get_argument("statistics", "-1")

        self.context.mode = mode
        self.context.receiver = receiver
        self.context.subordinate = subordinate
        self.context.direction = direction
        self.context.statistics = statistics

        rendering = self.is_rendering(starttime, endtime)
        if not rendering:
            return self.template()

        where = self.where_orders(starttime, endtime, mode, direction, receiver, subordinate, [1])
        warehouse = db.order.find(where).sort([ ("_id", -1) ]) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)

        result = self.userinofs_lists(warehouse)
        self.context.warehouse = result
        self.context.paging = paging.parse(self)
        self.context.paging.count = warehouse.count()

        if statistics == "1":
            self.context.ware = self.statistics_ware(where)
        else:
            self.context.ware = False

        return self.template()


@url("/order/historyinpuire")
class HistoryInpuire(HandlerBase):
    
    @tornado.web.authenticated
    def get_where(self, starttime, endtime, mode, direction, receiver, subordinate):
        result_list = [ Q('term', status=110) ]
        current_user = self.context.current_user
        reg = True
        if receiver:
            user = db.user.find_one({"userid" : receiver, "type" : 1})
            if user and current_user.relation in user.relation:
                result_list.append(Q('term', user=str(user._id)))
            else:
                reg = False
        elif subordinate:
            sub_user = db.user.find_one({"userid" : subordinate, "type" : 1})
            if sub_user and current_user.relation in sub_user.relation:
                result_list.append(Q('term', relation=sub_user.relation))
            else:
                reg = False
        else:
            result_list.append(Q('term', relation=current_user.relation))

        if not reg:
            result_list.append(Q('term', relation='///'))
        if mode != "-1":
            result_list.append(Q('term', mode=int(mode)))
        if direction != "-1":
            result_list.append(Q('term', direction=int(direction)))
        result_list.append(Q('range', created={'gte':starttime, 'lt':endtime, 'time_zone': '+08:00', 'format': 'yyyy-MM-dd HH:mm'}))
        q = Q('bool', filter=result_list)

        return q


    @tornado.web.authenticated
    def ela_order(self, starttime, endtime, mode, direction, receiver, subordinate, page):
        client = Elasticsearch()
        sea = Search(using=client, index="bots", doc_type='order').using(client)
        
        q = self.get_where(starttime, endtime, mode, direction, receiver, subordinate)
        s = sea.query(q)
        s.aggs.bucket("agg_sum", "terms", field="score").metric("money", "sum", field="money").pipeline("profit", "sum", \
                field="profit").pipeline("tax", "sum", field="tax")
        s = s.sort({'created': 'desc'})[ ((page-1)* DEFAULT_PAGESIZE) :  (page*DEFAULT_PAGESIZE) ]
        r = s.execute()
        return r


    @tornado.web.authenticated
    def get(self):
        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        mode = self.get_argument("mode", "-1")
        direction = self.get_argument("direction", "-1")
        receiver = self.get_argument("receiver", "")
        subordinate = self.get_argument("subordinate", "")
        page = self.get_argument('page', '1')

        self.context.mode = mode
        self.context.receiver = receiver
        self.context.subordinate = subordinate
        self.context.direction = direction

        rendering = self.is_rendering(starttime, endtime)
        if not rendering:
            return self.template()

        s = self.ela_order(starttime, endtime, mode, direction, receiver, subordinate, int(page))
        order_list = []
        for i in s.hits:
            order_id = i.meta.id
            i['_id'] = ObjectId(order_id)
            order = db.order.find_one({'_id': i['_id']})

            i['user_infos'] = self.redis_cache("user", str(i.user))
            i['assets'] = order.assets
            i['buyQoute'] = order.buyQoute
            i['endQoute'] = order.endQoute
            i['tax'] = order.tax
            i['expired'] = order.expired
            i['profit'] = order.profit
            i['created'] = order.created
            order_list.append(i)
        
        self.context.his_orders = order_list
        self.context.paging = paging.parse(self)
        self.context.paging.count = s.hits.total

        # 统计历史订单盈亏平金额和数量
        aggs_dict = []
        aggs_total = {}
        total_money = 0
        total_profit = 0
        total_count = 0
        total_tax = 0
        for i in s.aggregations.agg_sum.buckets:
            aggs_dict.append(i)
            total_money += i['money']['value']
            total_profit += i['profit']['value']
            total_count += i['doc_count']
            total_tax += i['tax']['value']

        aggs_total['total_money'] = total_money
        aggs_total['total_profit'] = total_profit
        aggs_total['total_tax'] = total_tax
        aggs_total['total_count'] = total_count

        self.context.aggs_total = aggs_total
        self.context.aggs_dict = aggs_dict
            
        return self.template()

    
    @tornado.web.authenticated
    def post(self):
        current_user_role = self.context.current_user_role
        if current_user_role != 'admin':
            return self.redirect("/user")

        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        mode = self.get_argument("mode", "-1")
        direction = self.get_argument("direction", "-1")
        receiver = self.get_argument("receiver", "")
        subordinate = self.get_argument("subordinate", "")

        if not starttime and not endtime:
            return self.redirect("/order/historyinpuire")

        try:
            q = self.get_where(starttime, endtime, mode, direction, receiver, subordinate)
            client = Elasticsearch()
            sea = Search(using=client, index="bots", doc_type='order').using(client)
            s = sea.query(q)

            self.set_header("Content-Type", "text/csv; charset=gbk")
            self.set_header("Content-Disposition", "attachment;filename=历史订单.csv")
            self.write("编号, 用户, 代理商, 资产, 投入金额, 方向, 模式, 下单价, 下单时间, 到期价, 手续费, 到期时间, 盈亏\r\n".decode('utf8').encode('gbk'))

            modes = { 0 : "短期期权", 1 : "长期", 2 : "60秒", 3 : "一触即付" }
            directions = { 1 : "买涨", 0 : "买跌", 2 : "未知", 4 : "还是未知" }
            o = datetime.timedelta(hours=-8)
            for i in s.sort({"created": "desc"})[0: s.count()]:
                order_id = i.meta.id
                order = db.order.find_one({'_id': ObjectId(order_id)})
                user_infos = self.redis_cache("user", str(order.user))
                starttime = (order.created - o).strftime("%Y-%m-%d %H:%M:%S")
                endtime = (order.expired - o).strftime("%Y-%m-%d %H:%M:%S")
                line = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}\n".format(order.no, '\t'+user_infos['userid'], '\t'+user_infos['parent_infos']['userid'], order.assets.name, round(order.money, 2), directions[order.direction], \
                        modes[order.mode], order.buyQoute,starttime, order.endQoute, round(order.tax, 2), endtime, round(order.profit, 2))
                self.write(line.decode('utf8').encode('gbk'))
            self.finish()
        except Exception, e:
            print e

