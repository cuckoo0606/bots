# -*- coding: utf-8 -*-

import redis
from tornado.options import options


class CacheMixin(object):

    @property
    def cache(self):
        if not hasattr(self, '_cache'):
            self._cache = redis.StrictRedis(host=options.REDIS_HOST, port=options.REDIS_PORT, db=options.REDIS_DB)
        return self._cache
