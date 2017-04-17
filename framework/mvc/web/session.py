#!/usr/lib/env python
#-*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-24

try:
    import cPickle as pickle
except ImportError:
    import pickle
import redis
import datetime
from uuid import uuid4


class Session(dict):
    """
        mvc session实现，支持会话数据持久化
    """

    def __init__(self, handler, sid=None, expires=None):
        self._handler = handler
        self._expires = expires
        self._sid = sid or self.generate_sid()
        self.load()


    @property
    def sid(self):
        return self._sid


    @property
    def handler(self):
        return self._handler


    def set_expires(self, expires):
        self._expies = expires


    def get_session(self, name):
        return self.get(name)


    def set_session(self, name, value):
        self[name] = value


    def del_session(self, name):
        del self[name]


    def load(self):
        value = self.handler.get_secure_cookie(self.sid)
        self.update(value and pickle.loads(value) or {})


    def save(self):
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=self._expires)
        self.handler.set_secure_cookie(self.sid, pickle.dumps(dict(self)), expires=expires)


    def generate_sid(self):
        sid = self.handler.get_cookie('sid')
        if not sid:
            sid = uuid4().get_hex()
            self.handler.set_cookie("sid", sid)
        
        return sid


class RedisSession(Session):
    """
        session会话数据redis持久化实现
    """
    def __init__(self, handler, sid=None, expires=30, host="localhost", port=6379):
        self._host = host
        self._port = port
        super(Session, self).__init__(handler, sid, expires)


    @property
    def host(self):
        return self._host


    @property
    def port(self):
        return self._port


    @property
    def prefixed(self):
        return '%s:%s' % ("session", self._sid)


    def load(self):
        r = redis.Redis(host=self.host, port=self.port)
        session = r.hgetall(self.prefixed)
        self.update(session)


    def save(self):
        r = redis.Redis(host=self.host, port=self.port)
        r.hmset(self.prefixed, self)
        r.expire(self.prefixed, self._expires * 60)

        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=self._expires)
        self.handler.set_secure_cookie("sid", self.sid, expires=expires)
