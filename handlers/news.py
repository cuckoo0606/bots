#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25

import os
import re
import datetime
import tornado.web
from bson import ObjectId
from cuckoo import per_result
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url, get_url
from framework.data.mongo import db, Document, DBRef


@url("/news/issue")
class NewsIssue(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["newsis"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        key = self.get_argument("key", "")
        self.context.key = key

        where = {}
        if key:
            where["$or"] = [{"title": {"$regex": key}},
                            {"content": {"$regex": key}}]

        self.context.paging = paging.parse(self)
        self.context.news = db.news.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.news.count()
        print '1'
        self.cache.delete("user*")

        return self.template()


@url("/news/classify")
class NewsClassify(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["newscl"]
        result = per_result(per, UP)

        if not result:
            return self.redirect("/account/signin")

        key = self.get_argument("key", "")
        self.context.key = key

        where = {}
        if key:
            where["$or"] = [{"classifyname": {"$regex": key}},
                            {"classifyid": {"$regex": key}}]

        self.context.paging = paging.parse(self)
        self.context.newsclassify = db.newsclassify.find(where) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.newsclassify.count()

        return self.template()


@url("/news/issue/edit")
class NewsIssueEdit(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["newsisa"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = ["newsism"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")

        self.context.news = db.news.find_one({"_id": ObjectId(id)})

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["newsisa"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})
        else:
            per = ["newsism"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

        title = self.get_argument("title", "")
        content = self.get_argument("content", "")

        if not title:
            return self.json({"status": "faild", "desc": "标题不能为空!"})

        if not content:
            return self.json({"status": "faild", "desc": "内容不能为空!"})

        try:
            news = Document()
            if id:
                news = db.news.find_one({"_id": ObjectId(id)})
                if not news:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                news._id = ObjectId(id)

            news.title = title
            news.content = content
            news.createtime = datetime.datetime.now()

            db.news.save(news)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "新增公告", "")

            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加公告", e.message)

            return self.json({"status": "faild", "desc": "未知错误!"})


@url("/news/classify/edit")
class NewsClassifyEdit(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["newscla"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")
        else:
            per = ["newsclm"]
            result = per_result(per, UP)

            if not result:
                return self.redirect("/account/signin")

        self.context.newsclassify = db.newsclassify.find_one(
            {"_id": ObjectId(id)})

        return self.template()

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", "") or None
        UP = self.context.UP

        if not id:
            per = ["newscla"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})
        else:
            per = ["newsclm"]
            result = per_result(per, UP)

            if not result:
                return self.json({"status": "faild", "desc": "您没有此权限!"})

        classifyid = self.get_argument("classifyid", "")
        classifyname = self.get_argument("classifyname", "")

        if not classifyname:
            return self.json({"status": "faild", "desc": "标题不能为空!"})

        if not classifyid:
            return self.json({"status": "faild", "desc": "标识不能为空!"})

        try:
            newsclassify = Document()
            if id:
                newsclassify = db.newsclassify.find_one({"_id": ObjectId(id)})
                if not newsclassify:
                    return self.json({"status": "faild", "desc": "修改的记录不存在!"})
            else:
                newsclassify._id = ObjectId(id)

            newsclassify.classifyname = classifyname
            newsclassify.classifyid = classifyid

            db.newsclassify.save(newsclassify)

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "新增公告", "")

            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "添加公告", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})
        return self.template()


@url("/news/issue/delete")
class NewsIssueDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["newsisd"]
        result = per_result(per, UP)

        if not result:
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        try:
            ids = self.get_argument("id", "").split(",")
            for i in ids:
                db.news.remove({"_id": ObjectId(i)})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除公告", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除公告", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})
        

@url("/news/classify/delete")
class NewsClassifyDelete(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        UP = self.context.UP
        per = ["newscld"]
        result = per_result(per, UP)

        if not result:
            return self.json({"status": "faild", "desc": "您没有此权限!"})

        try:
            ids = self.get_argument("id", "").split(",")
            for i in ids:
                db.newsclassify.remove({"_id": ObjectId(i)})

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "删除公告分类", "")
            return self.json({"status": "ok"})
        except Exception, e:
            print e
            self.system_record("系统", 0, "删除公告", e.message)
            return self.json({"status": "faild", "desc": "未知错误!"})