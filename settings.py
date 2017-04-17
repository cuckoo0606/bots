#!/usr/lib/env python
#-*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@hewoyi.com.cn
# Create Date: 2012-8-15


#
# MongoDB设置
#
# MongoDB地址
MONGODB_HOST = "127.0.0.1"
# MongoDB端口
MONGODB_PORT = 27017
# MongoDB库名
MONGODB_DB = "bots"
MONGODB_USER = ''
MONGODB_PASSWORD = ''


#
# WebServer设置
#

# WebServer端口
TORNADO_PORT = 8088
# COOKIE加密匙
COOKIE_SECRET = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
# 登陆页面
LOGIN_URL = "/account/signin"

#
# App设置
#

# 默认分页每页大小
DEFAULT_PAGESIZE = 15
permanent_session_lifetime = 30000
# session_redis ＝ {'host':'localhost', 'port':6379}

# 客户名
CUSTOMER = "TEST"
# 项目名(显示在左上角, 默认是'微交易')
PROJECT_NAME = '微交易'
# 代理模式(1:旧模式, 2:新模式, 默认是新模式)
AGENT_MODE = 2
# LOGO(登陆界面图片, icon为默认. 如客户许修改, 必须交图片给我)
PRO_ICON = "icon"

# 推荐码地址(将'localhost'换成ip地址)
HYPERLINK = "http://localhost:8866/"

#
# 佣金和红利设置:
#   模式: 1为旧模式, 2为新模式
#   周期: 1为即时, 2为每天
#   时间: 即时是秒, 每天是时间点
# 若留空或类型失败则以 "新模式 >> 即时 >> 10秒" 来计算

# 模式
CALCULATION_MODE = 2
# 周期
CALCULATION_CYCLE = 2
# 时间
# CALCULATION_TIME = 10
CALCULATION_TIME = "04:00"