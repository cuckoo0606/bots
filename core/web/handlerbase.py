#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Author: lixingtie
# Email: 260031207@qq.com
# Create Date: 2014-8-11


import json
import datetime
import requests
from bson import ObjectId
from tornado.util import ObjectDict
from framework.web import paging
from framework.mvc.web import RequestHandler
from framework.data.mongo import db, Document, DBRef

try:
    from personal import CUSTOMER
except Exception, e:
    try:
        from settings import CUSTOMER
    except Exception, e:
        CUSTOMER = ""

try:
    from personal import PROJECT_NAME
except Exception, e:
    try:
        from settings import PROJECT_NAME
    except Exception, e:
        PROJECT_NAME = None


class HandlerBase(RequestHandler):
    """
        页面处理器基类
        1. 显示当前用户
        2. 引用全局分页语句
        3. 读取当前用户权限
    """

    def initialize(self):
        id = self.get_current_user()
        current_user = self.redis_cache("user", id)
        current_user_role = current_user and "roleid" in current_user and current_user.roleid or ""
        # 获取权限
        permission_list = []
        if current_user_role:
            permissions = db.role.find_one({'roleid': current_user_role}).permission
            for i in permissions:
                p = db.permission.find_one({"_id": ObjectId(i)})
                if p:
                    permission_list.append(p['code'])
        projectname = PROJECT_NAME or "微交易"
        tcname = CUSTOMER == "SHANDONG" and "commission" or "红利"

        self.context.CUSTOMER = CUSTOMER
        self.context.tcname = tcname
        self.context.projectname = projectname
        self.context.paging = paging.parse(self)
        self.context.current_user = current_user
        self.context.current_user_role = current_user_role
        self.context.UP = permission_list
        self.context.func_time = self.func_time

        # 添加出金比例
        pay_rate = self.redis_cache("systemconfig", "exchange-pay-rate")
        self.context.exchange_pay_rate = pay_rate and pay_rate.value or 1

    def get_current_user(self):
        user = db.user.find_one({'_id': ObjectId(self.get_secure_cookie("u"))})
        return self.get_secure_cookie("u")

    def json(self, obj, content_type="text/json; charset=utf-8", cls=None):
        """
            输出json结果
        """
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls).replace("</", "<\\/"))

    def write_error(self, status_code, **kwargs):
        if status_code in [401, 403, 404, 500, 503]:
            kwargs["message"] = status_code
            self.render("error/401.html", **kwargs)
        else:
            self.write("BOOM!")

    def get_lower_user(self):
        """
            获取当前用户自己和自己的下级
        """
        current_user = self.context.current_user
        current_user_role = self.context.current_user_role
        relation = current_user and "relation" in current_user and current_user.relation or "//"

        if current_user_role == "admin":
            reg = "^/admin"
        else:
            reg = "^%s" % relation

        return reg

    def get_lower_notuser(self):
        """
            获取当前用户的下级
        """
        current_user = self.context.current_user
        current_user_role = self.context.current_user_role
        relation = current_user and "relation" in current_user and current_user.relation or "//"

        if current_user_role == "admin":
            reg_user = "^/admin/"
        else:
            reg_user = "^%s/" % relation

        return reg_user

    def system_record(self, user, logtype, operation, content):
        """
            搜集系统异常并写入系统日志
            字段:
                用户(DBRef/管理员/系统)
                类型 0(系统错误) 1(登陆记录) 2(资金变动) 3(用户操作[增删改]) 99(资金调整)
                模块
                操作
                内容
                时间 
                IP
        """
        if user not in ["管理员", "系统"]:
            user = DBRef("user", user)

        path = self.get_template_name()
        ip = self.request.remote_ip

        log = Document()
        log.user = user
        log.logtype = logtype
        log.module = "templates/" in path and path.split("templates/")[1] or path
        log.operation = operation
        log.content = content
        log.createtime = datetime.datetime.now()
        log.ip = ip

        db.systemlog.save(log)

    def redis_cache(self, key, value):
        '''
            在缓存找到结果
            添加userid, username, roleid, permission
        '''
        result = None
        redis_key = "{0}:{1}".format(key, value)
        result = self.cache.get(redis_key)
        if key == "user":
            if not result:
                result = db.user.find_one({'_id': ObjectId(value)})
                if result:
                    parent = "parent" in result and result.parent and result.parent.fetch() or None
                    parent_infos = {}
                    parent_infos['userid'] = parent and parent.userid or ""
                    parent_infos['username'] = parent and parent.username or ""
                    result["parent_infos"] = parent_infos
                    result["roleid"] = "userrole" in result and result.userrole and result.userrole.fetch().roleid or None
                    doc_result = ObjectDict(result)
                    self.cache.set(redis_key, doc_result, ex=60)
            else:
                result = ObjectDict(eval(result))
        elif key == "systemconfig":
            if not result:
                result = db.systemconfig.find_one({ "key": value })
                if result:
                    result = ObjectDict(result)
                    self.cache.set(redis_key, result, ex=60)
            else:
                result = ObjectDict(eval(result))

        return result


    def set_cache(self, key, value):
        '''
            主动更新缓存
        '''
        redis_key = "{0}:{1}".format(key, value)
        if key == "user":
            result = db.user.find_one({ "_id" : ObjectId(value) })
            if result:
                parent = "parent" in result and result.parent and result.parent.fetch() or None
                parent_infos = {}
                parent_infos['userid'] = parent and parent.userid or ""
                parent_infos['username'] = parent and parent.username or ""
                result["parent_infos"] = parent_infos
                result["roleid"] = "userrole" in result and result.userrole and result.userrole.fetch().roleid or None
                permissions = []
                for pid in result.userrole.fetch().permission:
                    p = db.permission.find_one({"_id": ObjectId(pid)})
                    if p:
                        permissions.append(p.code)
                result["permissions"] = permissions
                self.cache.set(redis_key, ObjectDict(result), ex=60)
                return True
        if key == "systemconfig":
            result = db.systemconfig.find_one({ "key" : value })
            if result:
                self.cache.set(redis_key, ObjectDict(result), ex=60)
                return True

        return False


    def get_date(self, type="default"):
        '''
            获取当天时间
        '''
        import time
        if type == "day":
            starttime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            endtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        else:
            starttime = time.strftime('%Y-%m-%d',time.localtime(time.time())) + " 00:00"
            endtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))    

        result = {"starttime" : starttime, "endtime" : endtime}

        return result


    def userinofs_lists(self, cursor, type="user"):
        '''
            通过mongodb游标, 循环添加用户信息
        '''
        result = []
        for i in cursor:
            i.user_infos = self.redis_cache("user", i[type])
            result.append(i)
        return result


    def is_rendering(self, starttime, endtime, type="default"):
        '''
            通过时间判断, 是否在页面渲染数据
            如果参数不齐全, 则直接返回
            如果不是管理员, 结束时间不能大于开始时间3天
        '''
        rendering = True
        if not starttime or not endtime:
            rendering = False
        else:
            if type == "day":
                select_start = datetime.datetime.strptime(starttime + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                select_end = datetime.datetime.strptime(endtime + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            else:
                select_start = datetime.datetime.strptime(starttime + ":00", "%Y-%m-%d %H:%M:%S")
                select_end = datetime.datetime.strptime(endtime + ":00", "%Y-%m-%d %H:%M:%S")

            if self.context.current_user_role != 'admin':
                days = (select_end - select_start).days
                if days > 3:
                    rendering = False

        if not rendering:
            today = self.get_date(type)
            self.context.starttime = today['starttime']
            self.context.endtime = today['endtime']
            self.context.show = False
        else:
            self.context.starttime = starttime
            self.context.endtime = endtime
            self.context.show = True

        return rendering

    
    def select_time(self, time_type, starttime, endtime, deltahours):
        ''' 
            根据传入的本地开始时间和结束时间, 转为utc时间的带毫秒的时间戳, 并返回一个字典
            time_type: timestamp和datetime
        '''
        import calendar
        result = {}
        delta = datetime.timedelta(hours=deltahours)
        if starttime:
            select_start = datetime.datetime.strptime(starttime + ":00", "%Y-%m-%d %H:%M:%S") - delta
            if time_type == "timestamp":
                select_start = calendar.timegm(select_start.utctimetuple()) * 1000
            result["$gte"] = select_start
        if endtime:
            select_end = datetime.datetime.strptime(endtime + ":00", "%Y-%m-%d %H:%M:%S") - delta
            if time_type == "timestamp":
                select_end = calendar.timegm(select_end.utctimetuple()) * 1000
            result["$lt"] = select_end

        return result


    def where_relation(self, receiver, subordinate):
        '''
            1,  根据传入的查询单一用户id和查询下级的用户id, 查出数据库的查询范围
            2,  查询的表必须有relation字段标记的表
            3,  注意权限和用户类型
            4,  规则定义:
                    1)  默认不查询
                    2)  如果输入的是查询单一用户, 并且存在这个用户, 则匹配这一用户
                    3)  如果输入的是查询用户下级, 并且存在这个用户, 则匹配这个用户的所有下级
                    4)  如果都没有输入, 则匹配当前用户以及下级
        '''
        result = "^///"
        current_user = self.context.current_user
        if receiver:
            user = db.user.find_one({"userid" : receiver, "type" : 1})
            if user and current_user.relation in user.relation:
                result = user.relation
        elif subordinate:
            sub_user = db.user.find_one({"userid" : subordinate, "type" : 1})
            if sub_user and current_user.relation in sub_user.relation:
                sub_reg = "^%s/" % sub_user.relation
                result = {"$regex" : "^" + sub_reg}
        else:
            result = {"$regex" : "^" + current_user.relation}
        return result


    def where_outflow(self, starttime, endtime, receiver, subordinate, status):
        '''
            出金表查询, 包括出金记录和出金申请的查询和导出
        '''
        where = {}
        if status and status != "0":
            where["status"] = int(status)

        select_time = self.select_time("datetime", starttime, endtime, 8)
        if select_time:
            where["created"] = select_time

        where["relation"] = self.where_relation(receiver, subordinate)

        return where


    def where_orders(self, starttime, endtime, mode, direction, receiver, subordinate, status):
        '''
            订单表查询, 包括历史订单的查询与导出和持仓单的查询
        '''
        where = {}
        where["status"] = {"$in" : status}
        where["relation"] = self.where_relation(receiver, subordinate)
        select_time = self.select_time("datetime", starttime, endtime, 8)
        if select_time:
            where["created"] = select_time

        # 通过模式查询
        if mode != "-1":
            where["mode"] = int(mode)

        # 通过方向查询
        if direction != "-1":
            direction = int(direction)
            where["direction"] = direction

        return where


    def where_com_pos(self, starttime, endtime, userid, key, status):
        '''
            佣金报表和红利报表的个人账单查询与导出
        '''
        where = {}
        where["type"] = status
        where["user"] = ObjectId(userid)
        select_time = {}

        select_time = self.select_time("datetime", starttime, endtime, 8)
        if select_time:
            where["created"] = select_time

        if key:
            where["remark"] = {"$regex": key}

        return where

    def func_time(self, time, delta_hours=0):
        delta = datetime.timedelta(hours=delta_hours)
        result = (time + delta).strftime("%Y-%m-%d %H:%M:%S")

        return result


def find_parents(user, parents):
    """
        查询非管理员的上级
    """
    if user and user.parent:
        try:
            parent = user.parent.fetch()
            if parent and parent.userrole.fetch().roleid != "admin":
                parents.append(parent)
                find_parents(parent, parents)
        except Exception as e:
            print e
            return []
    return parents
