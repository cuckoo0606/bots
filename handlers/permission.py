#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25

import os
import tornado.web
from bson import ObjectId
from cuckoo import per_result
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.data.mongo.escape import BSONEncoder
from framework.data.mongo import db, Document, DBRef


@url("/role")
class Role(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = [ "permissionro" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        self.context.permission = db.permission.find()
        self.context.paging = paging.parse(self)
        self.context.role = db.role.find() \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.role.count()

        return self.template()

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = [ "permissionroc" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        self.context.permission = db.permission.find()
        key = self.get_argument("key")

        self.context.role = db.role.find({"$or": [
            {"rolename": {"$regex": key}},
            {"roleid": {"$regex": key}},
        ]}) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)

        self.context.paging = paging.parse(self)
        self.context.paging.count = self.context.role.count()

        return self.template()


@url("/permission")
class Permission(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = [ "permissionpe" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        self.context.paging = paging.parse(self)
        self.context.permission = db.permission.find() \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.permission.count()

        return self.template()

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = [ "permissionpec" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        key = self.get_argument("key")

        self.context.permission = db.permission.find({"$or": [
            {"name": {"$regex": key}},
            {"code": {"$regex": key}},
        ]}) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)

        self.context.paging = paging.parse(self)
        self.context.paging.count = self.context.permission.count()

        return self.template()


@url("/role/edit")
class RoleEdit(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = [ "permissionroa" ]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = [ "permissionrom" ]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")

        self.context.role = db.role.find_one({"_id": ObjectId(id)})

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = [ "permissionroa" ]
            result = per_result(per, UP)

            if not result:
                return self.json({ "status" : "faild", "desc" : "您没有此权限!" })
        else:
            per = [ "permissionrom" ]
            result = per_result(per, UP)

            if not result:
                return self.json({ "status" : "faild", "desc" : "您没有此权限!" })

        rolename = self.get_argument("rolename", "")
        roleid = self.get_argument("roleid", "")

        if not rolename:
            return self.json({"status": "faild", "desc": "角色名称不能为空!"})

        if not roleid:
            return self.json({"status": "faild", "desc": "角色ID不能为空!"})

        try:
            role = Document()
            if id:
                role = db.role.find_one({"_id": ObjectId(id)})
                if not role:
                    return self.json({"status": "faild", "desc": "修改的角色不存在!"})
                if db.role.find_one({"roleid": roleid}) and roleid != role.roleid:
                    return self.json({"status": "faild", "desc": "此角色标识已存在!"})
                if role.roleid != roleid:
                    return self.json({"status": "faild", "desc": "标识码唯一, 不能修改!"})                  
                permission = role.permission
            else:
                if db.role.find_one({"roleid": roleid}):
                    return self.json({"status": "faild", "desc": "此角色标识已存在!"})
                role._id = ObjectId(id)
                permission = []

            role.rolename = rolename
            role.roleid = roleid
            role.permission = permission

            db.role.save(role)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加角色", "")
            return self.json({"status": "ok"})

        except Exception, e:
            print e
            self.system_record("系统", 0, "添加角色", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/permission/edit")
class PermissionEdit(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = [ "permissionpra" ]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = [ "permissionprm" ]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")

        self.context.permission = db.permission.find_one({"_id": ObjectId(id)})

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = [ "permissionpra" ]
            result = per_result(per, UP)

            if not result:
                return self.json({ "status" : "faild", "desc" : "您没有此权限!" })
        else:
            per = [ "permissionprm" ]
            result = per_result(per, UP)

            if not result:
                return self.json({ "status" : "faild", "desc" : "您没有此权限!" })

        name = self.get_argument("name", "")
        code = self.get_argument("code", "")

        if not name:
            return self.json({"status": "faild", "desc": "权限名称不能为空!"})

        if not code:
            return self.json({"status": "faild", "desc": "标识不能为空!"})

        try:
            permission = Document()
            if id:
                permission = db.permission.find_one({"_id": ObjectId(id)})
                if not permission:
                    return self.json({"status": "faild", "desc": "修改的权限不存在!"})
            else:
                permission._id = ObjectId(id)

            permission.name = name
            permission.name = code

            db.permission.save(permission)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "添加权限", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加权限", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/role/delete")
class RoleDelete(HandlerBase):

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = [ "permissionrod" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        ids = self.get_argument("id", "").split(",")
        if not ids:
            return self.json({"status": "faild", "desc": "请选择需要删除的数据!"})

        deleted = []

        try:
            for i in ids:
                if db.user.count({"userrole.$id": ObjectId(i)}) > 0:
                    continue

                deleted.append(i)
                db.role.remove({"_id": ObjectId(i)})

            if not deleted:
                return self.json({"status": "faild", "desc": "角色已被关联，未能删除!"})
            elif len(deleted) < len(ids):
                return self.json({"status": "warning", "desc": "没关联的角色已删除<br />部分角色已被关联，未能删除。"})
            else:
                return self.json({"status": "ok"})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除角色", "")
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除角色", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})

@url("/permission/delete")
class PermissionDelete(HandlerBase):

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = [ "permissionped" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        ids = self.get_argument("id", "").split(",")
        if not ids:
            return self.json({"status": "faild", "desc": "请选择需要删除的数据!"})

        deleted = []

        try:
            for i in ids:
                if db.role.count({"permission.$id": ObjectId(i)}) > 0:
                    continue

                deleted.append(i)
                db.permission.remove({"_id": ObjectId(i)})

            if not deleted:
                return self.json({"status": "faild", "desc": "角色已被关联，未能删除!"})
            elif len(deleted) < len(ids):
                return self.json({"status": "warning", "desc": "没关联的角色已删除<br />部分角色已被关联，未能删除。"})
            else:
                return self.json({"status": "ok"})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除权限", "")
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除权限", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/prset")
class Prset(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = [ "permissionpr" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        self.context.role = db.role.find()
        return self.template()

    @tornado.web.authenticated
    def post(self):
        UP = self.context.UP
        per = [ "permissionpra" ]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        tree = self.get_argument("tree", "").split(" ")
        roleid = self.get_argument("role", "")

        if not roleid:
            return self.json({"status": "faild", "desc": "角色还未选择!"})

        if tree == [""]:
            return self.json({"status": "faild", "desc": "角色权限不能为空!"})

        try:
            role = db.role.find_one({"_id": ObjectId(roleid)})
            if not role:
                return self.json({"status": "faild", "desc": "修改角色不存在!"})

            role.permission = tree
            db.role.save(role)
            # 需要清除所有用户的redis
            os.system('redis-cli -n 0 keys "*user:*"|xargs redis-cli -n 0 del')
            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "设置角色权限", "")

            return self.json({"status": "ok"})

        except Exception, e:
            print e
            self.system_record("系统", 0, "设置角色权限", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})

        self.redirect("/role")


@url("/prset/role/change")
class PrsetRoleChange(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        role = self.get_argument("role", "") or None
        permission = db.role.find_one({"_id": ObjectId(role)}).permission

        return self.json({"permission": permission})


@url("/prset/permission/show")
class PrsetpermissionShow(HandlerBase):

    def get(self):
        dict_pers = Document()
        pers = db.permission.find()

        for i in pers:
            p_id = str(i._id)
            pcode = i.permissionid
            dict_pers.setdefault(pcode, p_id)

        return self.json({"dict_pers": dict_per})


@url("/prset/permission/tree")
class PrsetpermissionShow(HandlerBase):

    def get_child_tree(self, parent=''):
        child = []
        for p in db.permission.find({'parrent': parent}):
            data = {'text': p.name, 'id': str(p._id)}
            nodes = self.get_child_tree(p._id)
            if len(nodes) > 0:
                data['nodes'] = nodes
            if str(p._id) in self.ps:
                data['state'] = {'selected': True}
            child.append(data)
        return child

    def get(self):
        self.ps = []
        roleid = self.get_argument('role', '')
        if roleid:
            role = db.role.find_one({'_id': ObjectId(roleid)})
            if role and role.permission:
                self.ps = role.permission
                
        return self.json(self.get_child_tree())
