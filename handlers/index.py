#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25

import os
import datetime
import tornado.web
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef
import re


@url("/")
class Index(HandlerBase):
    def get(self):
        return self.redirect("/home")
