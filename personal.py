#!/usr/lib/env python
#-*- encoding:utf-8 -*-

#
# MongoDB设置
#
MONGODB_URI = 'mongodb://dba:88T8jJrMw3UArvbo@dds-wz9a544cc81963c41.mongodb.rds.aliyuncs.com:3717,dds-wz9a544cc81963c42.mongodb.rds.aliyuncs.com:3717/bots?replicaSet=mgset-2893811'
# MongoDB地址
MONGODB_HOST = '127.0.0.1'
# MongoDB端口
MONGODB_PORT = 27017
# MongoDB库名
MONGODB_DB = 'bots'
MONGODB_USER = ''
MONGODB_PASSWORD = ''

#
# WebServer设置
#

# WebServer端口
TORNADO_PORT = 7017

#
# 客户设置
#

# 客户名
CUSTOMER = 'ZHUHAI_DINGSHENG'
# 项目名(显示在左上角, 默认是'微交易')
PROJECT_NAME = '恒亿微交易'
# 代理模式(1:旧模式, 2:新模式, 默认是新模式)
AGENT_MODE = 2
# LOGO(登陆界面图片, icon为默认. 如客户许修改, 必须交图片给我)
PRO_ICON = 'icon'
# 推荐码地址(将'localhost'换成ip地址)
HYPERLINK = 'http://weixin.leather-boss.com:8866/useredit?mode=3&route=2'

# 佣金和红利设置:
#   模式: 1为旧模式, 2为新模式
#   周期: 1为即时, 2为每天
#   时间: 即时是秒, 每天是时间点, 每周是星期几(1-7)[固定时间: 04:00]
# 模式
CALCULATION_MODE = 2
# 周期
CALCULATION_CYCLE = 1
# 时间
CALCULATION_TIME = 10
# CALCULATION_TIME = '04:00'
# 平单是否计算佣金(1:是[默认], -1:否)
SCORE = -1

#
# 出金设置
#

# 出金模式(1:不需银行处理(默认), 2:银行处理)
PAY_MODE = 1
# 出金类型(1: 汇潮)
PAY_TYPE = -1
