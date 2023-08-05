#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: memorystorage.py
# @time: 2019/7/29 15:40
# @Software: PyCharm


__author__ = 'A.Star'

from astar_wxsdk.session.sessionstorage import SessionStorage


class MemoryStorage(SessionStorage):

    def __init__(self):
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value, ttl=None):
        if value is None:
            return
        self._data[key] = value

    def delete(self, key):
        self._data.pop(key, None)
