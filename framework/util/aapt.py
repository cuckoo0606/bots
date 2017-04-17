#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-05

import os
import re
import zipfile
import commands


def dump_badging(path):
    cmd = "%s/aapt d badging %s" % (os.path.dirname(__file__), path)
    return commands.getoutput(cmd)
