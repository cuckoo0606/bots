#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-13

def url(handler, url):
    """
        生成URL
    """
    if not handler.request.arguments:
        return url

    kvs = {}
    for k, v in handler.request.arguments.items():
        kvs[k] = handler.get_argument(k)

    if "?" in url:
        qs = url[url.index("?") + 1:]
        url = url[:url.index("?")]

        for kv in qs.split("&"):
            kvs[kv[:kv.index("=")]] = kv[kv.index("=") + 1:]

    pars = []
    for k, v in kvs.items():
        pars.append("%s=%s" % (k, v))

    return "%s?%s" % (url, "&".join(pars))
