#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-13

try:
    from settings import DEFAULT_PAGESIZE
except:
    DEFAULT_PAGESIZE = 20


def skip(paging):
    if paging.index <= 1:
        return 0

    return paging.size * (paging.index - 1)

def parse(handler):
    """
        从页面参数中提取分页信息
    """
    info = Paging()
    size = handler.get_argument("size", "")
    if size and size.isdigit():
        info.size = int(size)

    page = handler.get_argument("page", "")
    if page and page.isdigit():
        info.index = int(page)

    return info


class Paging(object):
    """
        分页信息类
    """
    def __init__(self):
        self.size = DEFAULT_PAGESIZE
        self.index = 1
        self.count = 0
    
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = max(1, value)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = max(0, value)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = max(1, value)

    @property
    def prev(self):
        return max(1, self.index - 1)

    # 2016-6-3添加
    @property
    def last(self):
        last = self.pagecount
        return last

    @property
    def first(self):
        first = 1
        return first

    @property
    def next(self):
        return min(self.pagecount, self.index + 1)

    @property
    def pagecount(self):
        if self.size == 0:
            return 0
        
        return self.count / self.size + ((self.count % self.size) and 1 or 0)

    def as_dict(self):
        d = dict()
        d["size"] = self.size
        d["index"] = self.index
        d["prev"] = self.prev
        d["next"] = self.next
        d["next"] = self.next
        d["count"] = self.count
        d["pagecount"] = self.pagecount
        return d
