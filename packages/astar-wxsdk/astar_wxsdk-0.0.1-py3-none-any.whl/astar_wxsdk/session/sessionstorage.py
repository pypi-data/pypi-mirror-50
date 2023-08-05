#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: sessionstorage.py
# @time: 2019/7/29 15:41
# @Software: PyCharm


__author__ = 'A.Star'

from abc import ABCMeta, abstractmethod


class SessionStorage(metaclass=ABCMeta):

    @abstractmethod
    def get(self, key, default=None):
        pass

    @abstractmethod
    def set(self, key, value, ttl=None):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    def __getitem__(self, key):
        self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)
