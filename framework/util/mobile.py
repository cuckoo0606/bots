#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import json
import requests
try:
    from settings import MOBILEAREA_URL
except:
    MOBILEAREA_URL = "http://localhost:8751/mobile.html"


def area(mobile):
    """
        获取手机归属地
    """
    try:
        r = requests.get("%s?mobile=%s" % (MOBILEAREA_URL, mobile))
        if r.text and r.status_code == 200:
            r = json.loads(r.text)
        else:
            return { "mobile" : mobile, "city" : "", "region" : "", "isp" : "" }

        return { "mobile" : mobile, "city" : r["city"].strip(), "region" : r["region"].strip(), "isp" : r["isp"].strip() }
    except:
        return { "mobile" : mobile, "city" : "", "region" : "", "isp" : "" }


def paipai_area(mobile):
    """
        获取手机所在地
    """
    try:
        region = ""
        city = ""
        isp = ""

        r = requests.get("http://virtual.paipai.com/extinfo/GetMobileProductInfo?mobile={0}&amount=10000&callname=".format(mobile))
        if r.text and r.status_code == 200:
            m = re.search("province:'([^']*)'", r.text)
            if m:
                region = m.group(1)
            m = re.search("cityname:'([^']*)'", r.text)
            if m:
                city = m.group(1)
            m = re.search("isp:'([^']*)'", r.text)
            if m:
                isp = m.group(1)
        else:
            return { "mobile" : mobile, "city" : "", "region" : "", "isp" : "" }

        return { "mobile" : mobile, "city" : city, "region" : region, "isp" : isp }
    except:
        return { "mobile" : mobile, "city" : "", "region" : "", "isp" : "" }


if __name__ == "__main__":
    print paipai_area("13631482087")
