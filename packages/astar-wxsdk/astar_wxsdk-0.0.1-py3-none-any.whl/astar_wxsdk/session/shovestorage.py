#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: shovestorage.py
# @time: 2019/7/29 15:52
# @Software: PyCharm


__author__ = 'A.Star'

from astar_wxsdk.session.sessionstorage import SessionStorage


class ShoveStorage(SessionStorage):

    def __init__(self, shove, prefix='astarwxsdk'):
        self.shove = shove
        self.prefix = prefix

    def key_name(self, key):
        return '{0}:{1}'.format(self.prefix, key)

    def get(self, key, default=None):
        key = self.key_name(key)
        try:
            return self.shove[key]
        except KeyError:
            return default

    def set(self, key, value, ttl=None):
        if value is None:
            return

        key = self.key_name(key)
        self.shove[key] = value

    def delete(self, key):
        key = self.key_name(key)
        try:
            del self.shove[key]
        except KeyError:
            pass
