#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import zlib

def gzencode(text):
    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    return gzip_compress.compress(text) + gzip_compress.flush()


def gzdecode(text):
    return zlib.decompress(text, zlib.MAX_WBITS | 16)