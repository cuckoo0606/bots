#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-05

import io
import os
import re
import aapt
import hashlib
import zipfile
import commands


APPNAME_PATTERN = r"application\s*:\s*label\s*=\s*'(?P<appname>[^']+)'"
PACKNAME_PATTERN = r"package\s*:\s*name='(?P<packname>[^']+)'"
VERSION_PATTERN = r"versionName\s*=\s*'(?P<version>[^']+)'"
ICON_PATTERN = r"icon\s*=\s*'(?P<icon>[^']+)'"


def getinfo(path, save_icon_path=""):
    info = {}
    content = aapt.dump_badging(path)

    m = re.search(APPNAME_PATTERN, content)
    info["name"] = m and m.groups("appname")[0] or ""
    m = re.search(PACKNAME_PATTERN, content)
    info["packname"] = m and m.groups("packname")[0] or ""
    m = re.search(VERSION_PATTERN, content)
    info["version"] = m and m.groups("version")[0] or ""
    m = re.search(ICON_PATTERN, content)
    icon_path = m and m.groups("icon")[0] or "res/drawable-mdpi/icon.png"

    libsize = 0
    zip = zipfile.ZipFile(path, 'r') 
    for i in zip.infolist():
        if i.filename.startswith("lib/armeabi/"):
            libsize += i.file_size
        if save_icon_path and icon_path and i.filename == icon_path:
            (lambda f, d: (f.write(d), f.close()))(open(save_icon_path, 'wb'), zip.read(i.filename))

    info["apksize"] = os.path.getsize(path)
    info["libsize"] = libsize
    info["size"] = info["apksize"] + info["libsize"]
    info["md5"] = getmd5(path)
    return info


def getmd5(path):
    m = hashlib.md5()
    file = io.FileIO(path,'r')
    bytes = file.read(1024)
    while(bytes != b''):
        m.update(bytes)
        bytes = file.read(1024)

    file.close()
    return m.hexdigest()
