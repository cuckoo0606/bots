#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: hongyi
# Email: hongyi@hewoyi.com.cn
# Create Date: 2016-1-25

import os
import tornado.web
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.data.mongo import db
from bson import ObjectId
import re


@url("/profile")
class Profile(HandlerBase):
    @tornado.web.authenticated
    def get(self):
        return self.template()

