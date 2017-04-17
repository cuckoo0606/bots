#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-05

import json
import requests
try:
    from settings import IPAREA_URL
except:
    IPAREA_URL = "http://localhost:8750/ip.html"

def area(ip):
    """
        获取IP所在地
    """
    try:
        r = requests.get("%s?ip=%s" % (IPAREA_URL, ip))
        if r.text and r.status_code == 200:
            r = json.loads(r.text)
        else:
            return { "ip" : ip, "city" : "", "region" : "" }

        return { "ip" : ip, "city" : r["city"].strip(), "region" : r["region"].strip() }
    except:
        return { "ip" : ip, "city" : "", "region" : "" }


def taobao_area(ip):
    """
        获取IP所在地
    """
    try:
        r = requests.get("http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip)
        if r.text and r.status_code == 200:
            r = json.loads(r.text)
        else:
            return { "ip" : ip, "city" : "", "region" : "" }

        if isinstance(r["data"], dict):
            return { "ip" : ip, "city" : r["data"]["city"].strip(), "region" : r["data"]["region"].strip() }
        else:
            return { "ip" : ip, "city" : "", "region" : "" }
    except:
        return { "ip" : ip, "city" : "", "region" : "" }
