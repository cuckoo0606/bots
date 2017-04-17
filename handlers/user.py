#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25


import re
import os
import random
import datetime
import tornado.web

from bson import ObjectId
from cuckoo import per_result
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.util.security import md5
from framework.data.mongo import db, Document, DBRef

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


try:
    from personal import HYPERLINK
except Exception, e:
    HYPERLINK = ""

try:
    from personal import AGENT_MODE
except Exception, e:
    try:
        from settings import AGENT_MODE
    except Exception, e:
        AGENT_MODE = 2
try:
    from settings import DEFAULT_PAGESIZE
except:
    DEFAULT_PAGESIZE = 15

@url("/user")
class User(HandlerBase):

    @tornado.web.authenticated
    def ela_where_user(self, user_id, role_id, subordinate, page):
        current_user = self.context.current_user
        current_user_relation = current_user.relation

        result_list = [ Q('term', type=1) ]
        reg = True
        if subordinate:
            subordinate_user = db.user.find_one({"_id" : ObjectId(subordinate)})
            if subordinate_user and current_user_relation in subordinate_user.relation:
                # 只查下一级
                q = Q("match", parent=str(subordinate_user._id))
                result_list.append(q)
            else:
                reg = False
        elif user_id:
            user = db.user.find_one({"userid" : user_id})
            if user and current_user.relation in user.relation:
                # 只查询单用户
                q = Q('term', **{"userid.keyword" : user.userid})
                result_list.append(q)
            else:
                reg = False
        else:
            if self.context.current_user_role == "admin" and not (role_id and role_id != "0"): 
                admin_roleid = str(db.role.find_one({"roleid": "admin"})._id)
                q = Q("match", userrole=admin_roleid)
                result_list.append(q)
            else:
                reg_current_user_relation = current_user_relation + "(/[^/]+){0,1" + "}"
                q = Q('regexp', relation=reg_current_user_relation)
                result_list.append(q)

        if role_id and role_id != "0":
            q = Q("match", userrole=role_id)
            result_list.append(q)
        if not reg:
            result_list.append(Q("term", relation="///"))
        result = Q("bool", filter=result_list)

        client = Elasticsearch()
        sea = Search(using=client, index="user", doc_type='user').using(client)
        s = sea.query(result).sort({'created': 'desc'})[ ((page-1)* DEFAULT_PAGESIZE) : (page*DEFAULT_PAGESIZE) ]
        return s


    @tornado.web.authenticated
    def ela_aggs_user(self, user_id, subordinate):
        client = Elasticsearch()
        sea = Search(using=client, index="user", doc_type='user').using(client)
        result_list = [ Q('term', type=1) ]

        if subordinate:
            userid = ObjectId(subordinate)
        elif user_id and user_id != "0":
            check_user = db.user.find_one({'userid': user_id})
            if check_user:
                userid = check_user._id
            else:
                return False
        else:
            userid = self.context.current_user._id

        user = db.user.find_one({"_id" : userid})
        userrole = self.redis_cache("user", str(user._id)).roleid
        if userrole != "admin":
            reg_relation = "{0}(/[^/]+)*".format(user.relation)
            q = Q('regexp', relation=reg_relation)
            result_list.append(q)
        result = Q("bool", filter=result_list)
        s = sea.query(result)
        # 按角色统计金额和数量

        s.aggs.bucket("agg_sum", "terms", field="userrole.keyword").metric("amount", "sum", field="amount")
        r = s.execute()
        return r


    @tornado.web.authenticated
    def ela_where_subordinate(self):
        '''
            查询下一级用户的id, 管理员无视
        '''
        client = Elasticsearch()
        sea = Search(using=client, index="user", doc_type='user').using(client)
        result_list = [ Q('term', type=1) ]

        q = Q("match", parent=str(self.context.current_user._id))
        result_list.append(q)
        result = Q("bool", filter=result_list)
        s = sea.query(result)

        return s


    def get(self):
        UP = self.context.UP
        per = ["user"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        role_id = self.get_argument("role_id", "0")
        user_id = self.get_argument("user_id", "")
        subordinate = self.get_argument("subordinate", "")
        statistics = self.get_argument("statistics", "-1")
        page = self.get_argument("page", "1")

        newurl = self.request.uri
        status_url = "?" in newurl and newurl.split("?")[1] or ""
        roles = [ i for i in db.role.find() ]

        # ela查询分页用户
        s = self.ela_where_user(user_id, role_id, subordinate, int(page))
        result_users = []
        for i in s:
            u = db.user.find_one({"userid": i.userid})

            user = {}
            user['_id'] = u._id
            user['user_infos'] = self.redis_cache("user", str(u._id))
            user['brokerage'] = "brokerage" in u and u.brokerage or 0
            user['position'] = "position" in u and u.position or 0
            user['userrole'] = "userrole" in u and u.userrole and u.userrole.fetch().rolename or ""
            user['amount'] = round(u.amount, 2)
            user['status'] = 'status' in u and u.status or 0
            user['created'] = u.created

            result_users.append(user)

        # ela统计
        aggs_user = self.ela_aggs_user(user_id, subordinate)
        roles_dict = {}
        for i in roles:
            roles_dict[str(i._id)] = i. rolename

        aggs_result = []
        if aggs_user:
            for i in aggs_user.aggregations.agg_sum.buckets:
                aggs_one = {}
                for k in roles_dict.keys():
                    if k in i.key:
                        aggs_one['rolename'] = roles_dict[k]
                        break

                aggs_one['count'] = i.doc_count
                aggs_one['amount'] = round(i.amount.value, 2)
                aggs_result.append(aggs_one)

        # 显示出金手续费
        pay_type = self.redis_cache("systemconfig", "pay-handling-type")
        pay_handling_type = pay_type and pay_type.value or None
        handling_charge = 0
        if pay_handling_type:
            if pay_handling_type == "0":
                handling_percent = self.redis_cache("systemconfig", "pay-handling-percent")
                handling_charge = handling_percent and handling_percent.value or 0
                handling_charge = "{0}%".format(handling_charge)
            elif pay_handling_type == "1":
                handling_amount = self.redis_cache("systemconfig", "pay-handling-amount")
                handling_charge = handling_amount and handling_amount.value or 0

        # 设置比例用户显示限制
        sub = self.ela_where_subordinate()
        ratio_users = []
        for i in sub.scan():
            ratio_users.append(i.userid)
        
        self.context.handling_charge = handling_charge
        self.context.user_id = user_id
        self.context.user = result_users
        self.context.roles = roles
        self.context.role_id = role_id
        self.context.newurl = newurl
        self.context.statistics = statistics
        self.context.status_url = status_url
        self.context.paging = paging.parse(self)
        self.context.paging.count = s.count()
        self.context.statistics_list = aggs_result
        self.context.ratio_users = ratio_users
        return self.template()


def editcode():
    '''
        随机生成6位推荐码
        由数字和小写字母组合
    '''
    str_code = "0123456789abcdefghijklmnopqrstuvwxyz"
    code = "".join([i for i in random.sample(str_code, 6)])
    faildcode = db.user.find_one({"referralcode" : code})
    if faildcode:
        editcode()
    else:
        return code


@url("/user/edit")
class UserEdit(HandlerBase):
    '''
        1, 创建时间不能被更改
        2, 权限: 只能修改自己下级的
    '''
    @tornado.web.authenticated
    def check_reg(self, userid):
        current_user = self.context.current_user
        current_user_role = self.context.current_user_role
        try:
            user = db.user.find_one({"_id" : ObjectId(userid)})
            if current_user_role != "admin":
                if current_user.relation not in user.relation:
                    return False
            return True
        except:
            return False


    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["usera"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = ["userm"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")

            result_reg = self.check_reg(id)
            if not result_reg:
                return self.redirect("/account/signin")

        current_user_role = self.context.current_user_role

        if current_user_role == "admin":
            role = db.role.find()
        elif current_user_role == "member":
            role = db.role.find({"roleid" : "member"})
        else:
            role = db.role.find({"roleid": {"$nin": ["admin"]}})        

        user = db.user.find_one({"_id" : ObjectId(id)})
        # user = self.redis_cache("user", id)

        self.context.user = user
        self.context.role = role
        self.context.usergroup = db.usergroup.find()
        self.context.level = db.level.find()

        hyperlink = user and "{0}&code={1}".format(HYPERLINK, user.referralcode) or ""
        self.context.hyperlink = hyperlink

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["usera"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

            temp_remark = "添加用户"
        else:
            per = ["userm"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

            result_reg = self.check_reg(id)
            if not result_reg:
                return self.json({"status": "faild", "desc": "您没有此权限!"})
            temp_remark = "修改用户"

        userid = self.get_argument("userid", "")
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        IDcard = self.get_argument("IDcard", "")
        email = self.get_argument("email", "")
        address = self.get_argument("address", "")
        sex = self.get_argument("sex", "")
        phone = self.get_argument("phone", "")
        userrole = self.get_argument("userrole", "")
        totalbets = self.get_argument("totalbets", 0)
        bankholder = self.get_argument("bankholder", "")
        bank = self.get_argument("bank", "")
        bankId = self.get_argument("bankId", "")
        bankbranch = self.get_argument("bankbranch", "")
        bankaccount = self.get_argument("bankaccount", "")
        province = self.get_argument("province", "")
        city = self.get_argument("city", "")

        current_user = self.context.current_user
        current_user_role = self.context.current_user_role
        if current_user_role == "admin":
            usergroup = self.get_argument("usergroup", "")
            level = self.get_argument("level", "")

        if not userid:
            return self.json({"status": "faild", "desc": "注册名不能为空!"})

        if not username:
            return self.json({"status": "faild", "desc": "用户名称不能为空!"})

        if not userrole:
            return self.json({"status": "faild", "desc": "用户角色不能为空!"})

        if not id:
            if not password:
                return self.json({"status": "faild", "desc": "用户密码不能为空!"})

        if not phone:
            return self.json({"status": "faild", "desc": "手机号码不能为空!"})

        reg_phone = r"^(13[0-9]|15[012356789]|17[01678]|18[0-9]|14[57])[0-9]{8}$"
        if not re.match(reg_phone, phone):
            return self.json({"status": "faild", "desc": "手机号码格式不正确!"})

        reg_userid = r'[A-Za-z0-9]{1,}$'
        if not re.match(reg_userid, userid):
            return self.json({"status": "faild", "desc": "注册名不符合规则！"})

        if bankaccount:
            reg_bankaccount = r'^\d{1,}$'
            if not re.match(reg_bankaccount, bankaccount):
                return self.json({"status": "faild", "desc": "银行账号只能输入数字！"})

        if not id and db.user.find_one({"userid": userid}):
            return self.json({"status": "faild", "desc": "用户编号已存在!"})

        try:
            totalbets = totalbets and float(totalbets) or ""
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "%s,总盘口格式不正确!" % tc})

        try:
            content = {}
            if id:
                # 被修改的用户
                user = db.user.find_one({"_id": ObjectId(id)})
                user_rolename = user.userrole.fetch().roleid

                content["old_user"] = db.user.find_one({"_id": ObjectId(id)})
                if not user:
                    return self.json({"status": "faild", "desc": "修改的用户不存在!"})
                if user.userid != userid:
                    return self.json({"status": "faild", "desc": "用户标识码唯一, 不能修改!"})

                role_admin = db.role.find_one({"roleid" : "admin"})._id
                role_agent = db.role.find_one({"roleid" : "agent"})._id
                role_member = db.role.find_one({"roleid" : "member"})._id

                # 如果角色变更
                if userrole != str(user.userrole.id):
                    if user._id == current_user['_id']:
                        return self.json({"status": "faild", "desc": "不可更改自己的角色!"})
                    # 管理员角色不可换
                    if user_rolename == "admin":
                        if userrole != str(role_admin):
                            return self.json({"status": "faild", "desc": "管理员角色不可更改!"})
                    else:
                        if userrole == str(role_admin):
                            return self.json({"status": "faild", "desc": "角色不可更改为管理员!"})

                    # 如果当前用户不是管理员. 则只有代理商可以更改代理商和会员的角色
                    if current_user_role not in [ "agent", "admin" ]:
                        return self.json({"status": "faild", "desc": "无权限更改角色!"})
                    elif current_user_role == "agent":
                        if userrole not in [ str(role_agent), str(role_member) ]:
                            return self.json({"status": "faild", "desc": "无权限更改为此角色!"})

            else:
                user = Document()
                # 新增的用户, 如果是管理员则可以指定代理商, 否则只能新用户上级是自己
                content["old_user"] = {}
                user.amount = 0
                user._id = ObjectId()

                user_role = db.role.find_one({"_id" : ObjectId(userrole)})
                user_roleid = user_role and user_role.roleid or ""

                if current_user_role == "admin":
                    if user_roleid == "admin":
                        user.relation = "/admin"
                        user.parent = ""
                    else:
                        agent = self.get_argument("agent", "")
                        agent_user = db.user.find_one({ "userid" : agent })
                        if agent_user:
                            user.relation = agent_user.relation + "/" + str(user._id)
                            user.parent = DBRef("user", agent_user._id)
                        else:
                            return self.json({"status": "faild", "desc": "无此代理商用户id, 无法绑定上级!"})
                else:
                    user.relation = current_user['relation'] + "/" + str(user._id)
                    user.parent = DBRef("user", current_user['_id'])

                user.created = datetime.datetime.now()
                user.referralcode = editcode()
            if id:
                if password and current_user_role == "admin":
                    user.password = md5(password)
            else:
                user.password = md5(password)

            user.userid = userid
            user.username = username
            user.IDcard = IDcard
            user.bankholder = bankholder
            user.bank = bank
            user.bankId = bankId
            user.bankbranch = bankbranch
            user.bankaccount = bankaccount
            user.province = province
            user.city = city
            user.email = email
            user.address = address
            user.sex = sex
            user.phone = phone
            # 真实客户
            user.type = 1
            user.totalbets = totalbets
            user.userrole = DBRef("role", ObjectId(userrole))
            if current_user_role == "admin":
                if usergroup:
                    user.usergroup = DBRef("usergroup", ObjectId(usergroup))
                else:
                    user.usergroup = ""
                if level:
                    user.level = DBRef("level", ObjectId(level))
                else:
                    user.level = ""
            if not id:
                # 初始化交易状态
                if user_roleid == "member":
                    status = db.systemconfig.find_one({ "key" : "member-status" })
                    try:
                        member_group = db.systemconfig.find_one({ "key" : "member-group" })
                        group = member_group and member_group.value or "-1"
                        if group != "-1":
                            user.usergroup = DBRef("usergroup", ObjectId(group))
                    except:
                        return self.json({"status": "faild", "desc": "没有此用户组!"})
                elif user_roleid == "agent":
                    status = db.systemconfig.find_one({ "key" : "agent-status" })
                else:
                    status = db.systemconfig.find_one({ "key" : "other-status" })

                user.status = status and status.value or 0

            content["new_user"] = user

            db.user.save(user)
            self.system_record(current_user._id, 3, temp_remark, content)

            # 更新缓存
            result = self.set_cache("user", id)
            if not result:
                self.system_record("系统", 0, "添加用户", "更新缓存失败")

            return self.json({"status": "ok"})

        except Exception, e:
            print e
            self.system_record("系统", 0, "添加用户", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/usergroup")
class UserGroup(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["usergroup"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")

        key = self.get_argument("key", "")

        where = {}
        if key:
            where["groupname"] = {"$regex" : key}

        self.context.key = key
        self.context.paging = paging.parse(self)
        self.context.usergroup = db.usergroup.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)

        self.context.paging.count = self.context.usergroup.count()

        return self.template()


@url("/usergroup/edit")
class UserGroupEdit(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["usergroup"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")
        id = self.get_argument("id", "") or None

        self.context.usergroup = db.usergroup.find_one({"_id" : ObjectId(id)})

        return self.template()

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = ["usergroup"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")

        id = self.get_argument("id", "") or None

        groupname = self.get_argument("groupname", "")
        groupcode = self.get_argument("groupcode", "")

        if not groupname:
            return self.json({"status": "faild", "desc": "用户组名称不能为空!"})

        if not groupcode:
            return self.json({"status": "faild", "desc": "用户组标识不能为空!"})

        try:
            usergroup = Document()
            if id:
                usergroup = db.usergroup.find_one({"_id": ObjectId(id)})
                if not usergroup:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                usergroup._id = ObjectId(id)

            usergroup.groupname = groupname
            usergroup.groupcode = groupcode

            db.usergroup.save(usergroup)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加用户组", "")

            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加用户组", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/level")
class Level(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["level"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")

        key = self.get_argument("key", "")

        where = {}
        if key:
            where["name"] = {"$regex" : key}

        self.context.key = key
        self.context.paging = paging.parse(self)
        self.context.level = db.level.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.level.count()

        return self.template()

@url("/level/edit")
class LevelEdit(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["level"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")

        id = self.get_argument("id", "") or None

        self.context.level = db.level.find_one({"_id" : ObjectId(id)})

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None

        name = self.get_argument("name", "")
        code = self.get_argument("code", "")
        odds = self.get_argument("odds", 0)
        maximum = self.get_argument("maximum", 0)
        minimum = self.get_argument("minimum", 0)

        if not name:
            return self.json({"status": "faild", "desc": "名称不能为空!"})

        if not code:
            return self.json({"status": "faild", "desc": "标识不能为空!"})

        if not odds:
            return self.json({"status": "faild", "desc": "比例不能为空!"})

        try:
            odds = float(odds)
        except Exception, e:
            return self.json({"status": "faild", "desc": "比例不合法!"})

        try:
            maximum = float(maximum)
            minimum = float(minimum)
            if maximum <= minimum:
                return self.json({"status": "faild", "desc": "最大值要大于最小值!"})
        except Exception, e:
            return self.json({"status": "faild", "desc": "最大值或最小值不合法!"})

        try:
            level = Document()
            if id:
                level = db.level.find_one({"_id": ObjectId(id)})
                if not level:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                level._id = ObjectId(id)

            level.name = name
            level.code = code
            level.odds = odds
            level.maximum = maximum
            level.minimum = minimum

            db.level.save(level)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加用户级别", "")

            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加用户级别", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/user/delete")
class UserDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["userd"]
        result = per_result(per, UP)

        if not result:
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        try:
            ids = self.get_argument("id").split(",")
            if ids == [""]:
                return self.json({"status": "faild", "desc": "请选择需要删除的数据"})

            deleted = []

            for i in ids:
                i_relation = db.user.find_one({"_id": ObjectId(i)}).relation
                reg = "^%s/" % i_relation
                where = {}
                where["user"] = ObjectId(i)

                if db.user.count({"relation": {"$regex": reg}}) > 0 or db.books.count(where) > 0 or db.order.count({"user": ObjectId(i)}) > 0:
                    continue

                deleted.append(i)
                db.user.remove({"_id": ObjectId(i)})

            if not deleted:
                return self.json({"status": "faild", "desc": "选择的用户已被关联!"})
            elif len(deleted) < len(ids):
                return self.json({"status": "warning", "desc": "没关联的用户已删除<br />部分用户已被关联，未能删除。"})
            else:
                return self.json({"status": "ok"})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除用户", "")
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除用户", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/usergroup/delete")
class UserGroupDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["usergroup"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")
        try:
            ids = self.get_argument("id").split(",")
            if ids == [""]:
                return self.json({"status": "faild", "desc": "请选择需要删除的数据"})

            deleted = []

            for i in ids:
                if db.user.count({"usergroup.$id": ObjectId(i)}) > 0:
                    continue

                deleted.append(i)
                db.usergroup.remove({"_id": ObjectId(i)})

            if not deleted:
                return self.json({"status": "faild", "desc": "选择的用户组已被关联!"})
            elif len(deleted) < len(ids):
                return self.json({"status": "warning", "desc": "没关联的用户组已删除<br />部分用户组已被关联，未能删除。"})
            else:
                return self.json({"status": "ok"})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除用户组", "")
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除用户组", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/level/delete")
class LevelDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["level"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")
        try:
            ids = self.get_argument("id").split(",")
            if ids == [""]:
                return self.json({"status": "faild", "desc": "请选择需要删除的数据"})

            deleted = []

            for i in ids:
                if db.user.count({"level.$id": ObjectId(i)}) > 0:
                    continue

                deleted.append(i)
                db.level.remove({"_id": ObjectId(i)})

            if not deleted:
                return self.json({"status": "faild", "desc": "选择的用户组已被关联!"})
            elif len(deleted) < len(ids):
                return self.json({"status": "warning", "desc": "没关联的用户组已删除<br />部分用户组已被关联，未能删除。"})
            else:
                return self.json({"status": "ok"})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除用户组级别", "")
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除用户级别", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/user/status")
class UserStatus(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["status"]
        result = per_result(per, UP)
        if not result:
            return self.write("该角色没有此权限!")

        id = self.get_argument("id", "") or None
        role_id = self.get_argument("role_id", "0")
        user_id = self.get_argument("user_id", "")
        subordinate = self.get_argument("subordinate", "")

        if not id:
            return self.json({"status": "faild", "desc": "未找到用户!"})
        user = db.user.find_one({"_id" : ObjectId(id)})
        if not user:
            return self.json({"status": "faild", "desc": "未找到用户!"})
        if "type" not in user:
            return self.json({"status": "faild", "desc": "用户类型异常!"})
        user_type = user.type
        if user_type not in [1, 2]:
            return self.json({"status": "faild", "desc": "用户类型异常!"})

        try:
            status = "status" in user and user.status or ""
            kvs = {0 : 1, 1 : 0}
            if not status:
                newstatus = 1
            else:
                newstatus = kvs[status]

            db.user.update({"_id" : user._id}, {"$set" : {"status" : newstatus}})
            self
            if user_type == 1:
                url = "/user?role_id=" + role_id + "&user_id=" + user_id + "&subordinate=" + subordinate
            else:
                url = "/simulation"
            return self.redirect(url)
        except Exception, e:
            print e


@url("/simulation")
class Simulation(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        user_id = self.get_argument("user_id", "0")

        where = {}
        where["type"] = 2
        if user_id != "0":
            user = db.user.find_one({"_id" : ObjectId(user_id), "type" : 2})
            if not user:
                return self.json({"status": "faild", "desc": "未找到此用户!"})
            where["_id"] = ObjectId(user_id)

        self.context.users = db.user.find({"type" : 2})
        self.context.user_id = user_id
        self.context.newurl = "/simulation"

        self.context.paging = paging.parse(self)
        self.context.simulation_users = db.user.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.simulation_users.count()

        return self.template()


@url("/simulation/delete")
class SimulationDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        current_user = self.context.current_user
        current_user_role = self.context.current_user_role
        if current_user_role != "admin":
            self.json({"status": "faild", "desc": "该角色没有此权限!"})
        try:
            ids = self.get_argument("id").split(",")
            if ids == [""]:
                return self.json({"status": "faild", "desc": "请选择需要删除的数据"})

            for i in ids:
                db.user.remove({"_id" : ObjectId(i), "type" : 2})

            self.system_record(current_user._id, 3, "删除虚拟用户", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除虚拟用户", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


# 佣金设置
@url("/user/setcom")
class UserSetcom(HandlerBase):
    @tornado.web.authenticated
    def check_commission(self, user, commission):
        try:
            parent = "parent" in user and user.parent and user.parent.fetch() or ""
            if parent and parent.userrole.fetch().roleid != "admin":
                p_commission = "brokerage" in parent and parent.brokerage or 0
                if commission > p_commission:
                    msg = "不能大于上级佣金: {0}!".format(p_commission)
                    return False, msg
            reg = "^%s/" % user.relation
            users = db.user.find({"relation" : {"$regex" : reg}, "brokerage" : {"$exists" : True}})
            if users.count() > 0:
                coms = [ i.brokerage for i in users ]
                max_com = max(coms)
                if commission < max_com:
                    msg = "不能小于下级佣金: {0}!".format(max_com)
                    return False, msg

            return True, "OK"
        except Exception, e:
            print e
            msg = "未知错误"
            return False, msg


    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = ["com_ratio"]
        result = per_result(per, UP)
        if not result:
            return self.json({"status": "faild", "desc": "没有此权限!"})

        user_id = self.get_argument("user_id", "")
        commission = self.get_argument("commission", "")

        if not user_id:
            return self.json({"status": "faild", "desc": "用户有误!"})
        user = db.user.find_one({"_id" : ObjectId(user_id)})
        if not user:
            return self.json({"status": "faild", "desc": "未找到此用户!"})

        old_com = "brokerage" in user and user.brokerage or 0

        try:
            commission = round(float(commission), 2)
            if commission < 0:
                return self.json({"status": "faild", "desc": "佣金比例需大于0!"})
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "佣金比例格式错误!"})

        try:
            # 除了管理员, 上级只能设置下一级
            current_user = self.context.current_user
            current_user_role = self.context.current_user_role

            if current_user_role != "admin":
                try:
                    if user.parent.fetch()._id != current_user._id:
                        return self.json({"status": "faild", "desc": "不能设置非下一级的用户!"})
                except Exception, e:
                    print e
                    return self.json({"status": "faild", "desc": "设置失败!"})

            if user._id == current_user._id:
                return self.json({"status": "faild", "desc": "不能修改自己的佣金!"})

            # 新模式限制(山东)
            if AGENT_MODE == 2:
                roleid = user.userrole.fetch().roleid
                if roleid == "admin":
                    return self.json({"status": "faild", "desc": "管理员没有佣金!"})

                result, msg = self.check_commission(user, commission)

                if result:
                    # 更新数据库
                    db.user.update({"_id" : user._id}, {"$set" : {"brokerage" : commission}})
                    self.system_record(current_user._id, 3, "设置佣金", {"user" : user._id, "old_com" : old_com, "new_com" : commission})
                    return self.json({"status": "ok"})
                else:
                    return self.json({"status": "faild", "desc": msg})
            else:
                db.user.update({"_id" : user._id}, {"$set" : {"brokerage" : commission}})
                self.system_record(current_user._id, 3, "设置佣金", {"user" : user._id, "old_com" : old_com, "new_com" : commission})
                return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "设置佣金", e.message)
            return self.json({"status": "faild", "desc": "未知错误"})


# 红利设置
@url("/user/setpos")
class UserSetpos(HandlerBase):
    @tornado.web.authenticated
    def check_position(self, user, position):
        '''
            检测佣金比例:
                1, 若上级不是管理员, 则佣金要比上级的少
                2, 若存在下级, 则佣金要比所有的下级都大
        '''
        try:
            parent = "parent" in user and user.parent and user.parent.fetch() or ""
            if parent and parent.userrole.fetch().roleid != "admin":
                p_position = "position" in parent and parent.position or 0
                if position > p_position:
                    msg = "不能大于上级红利: {0}!".format(p_position)
                    return False, msg
            reg = "^%s/" % user.relation
            users = db.user.find({"relation" : {"$regex" : reg}, "position" : {"$exists" : True}})
            if users.count() > 0:
                pos = [ i.position for i in users ]
                max_pos = max(pos)
                if position < max_pos:
                    msg = "不能小于下级红利: {0}!".format(max_pos)
                    return False, msg

            return True, "OK"
        except Exception, e:
            print e
            msg = "未知错误"
            return False, msg

    @tornado.web.authenticated
    def post(self):
        '''
            上级只能设置下一级

            新分配模式:
                1, 管理员不能设置
                2, 本人不能设置
                3, 遵守上级大于等于下级
            旧分配模式:
                随便修改
        '''
        UP = self.context.UP
        per = ["pos_ratio"]
        result = per_result(per, UP)
        if not result:
            return self.json({"status": "faild", "desc": "没有此权限!"})
        user_id = self.get_argument("user_id", "")
        position = self.get_argument("position", "")

        if not user_id:
            return self.json({"status": "faild", "desc": "用户有误!"})
        user = db.user.find_one({"_id" : ObjectId(user_id)})
        if not user:
            return self.json({"status": "faild", "desc": "未找到此用户!"})

        old_pos = "position" in user and user.position or 0

        try:
            position = round(float(position), 2)
            if position < 0:
                return self.json({"status": "faild", "desc": "红利比例需大于0!"})
        except Exception, e:
            print e
            return self.json({"status": "faild", "desc": "红利比例格式错误!"})

        try:
            # 除了管理员, 上级只能设置下一级
            current_user = self.context.current_user
            current_user_role = self.context.current_user_role

            if current_user_role != "admin":
                try:
                    if user.parent.fetch()._id != current_user._id:
                        return self.json({"status": "faild", "desc": "不能设置非下一级的用户!"})
                except Exception, e:
                    print e
                    return self.json({"status": "faild", "desc": "设置失败!"})

            if user._id == current_user._id:
                return self.json({"status": "faild", "desc": "不能修改自己的红利!"})

            # 新模式限制(山东)
            if AGENT_MODE == 2:
                roleid = user.userrole.fetch().roleid
                if roleid == "admin":
                    return self.json({"status": "faild", "desc": "管理员没有红利!"})

                result, msg = self.check_position(user, position)

                if result:
                    # 更新数据库
                    db.user.update({"_id" : user._id}, {"$set" : {"position" : position}})
                    self.system_record(current_user._id, 3, "设置红利", { "user" : user._id, "old_pos" : old_pos, "new_pos" : position })
                    return self.json({"status": "ok"})
                else:
                    return self.json({"status": "faild", "desc": msg})
            else:
                db.user.update({"_id" : user._id}, {"$set" : {"position" : position}})
                self.system_record(current_user._id, 3, "设置红利", { "user" : user._id, "old_pos" : old_pos, "new_pos" : position })
                return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "设置红利", e.message)
            return self.json({"status": "faild", "desc": "未知错误"})
