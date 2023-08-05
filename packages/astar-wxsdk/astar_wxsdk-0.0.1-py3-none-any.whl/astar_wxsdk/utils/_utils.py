#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: _utils.py
# @time: 2019/7/26 15:30
# @Software: PyCharm


__author__ = 'A.Star'

try:
    '''Use simplejson if we can, fallback to json otherwise.'''
    import simplejson as json
except ImportError:
    import json  # NOQA

import six.moves.urllib.parse as urlparse

from pysmx.crypto import hashlib

try:
    '''Use simplejson if we can, fallback to json otherwise.'''
    import simplejson as json
except ImportError:
    import json  # NOQA

import six


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


class WxSigner(object):
    """WeChat data signer"""

    def __init__(self, delimiter=b''):
        self._data = []
        self._delimiter = to_binary(delimiter)

    def add_data(self, *args):
        """Add data to signer"""
        for data in args:
            self._data.append(to_binary(data))

    @property
    def signature(self):
        """Get data signature"""
        self._data.sort()
        str_to_sign = self._delimiter.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()


def check_signature(token, signature, timestamp, nonce):
    """Check WeChat callback signature, raises InvalidSignatureException
    if check failed.

    :param token: WeChat callback token
    :param signature: WeChat callback signature sent by WeChat server
    :param timestamp: WeChat callback timestamp sent by WeChat server
    :param nonce: WeChat callback nonce sent by WeChat sever
    """
    signer = WxSigner()
    signer.add_data(token, timestamp, nonce)
    if signer.signature != signature:
        from wechatpy.exceptions import InvalidSignatureException

        raise InvalidSignatureException()


def check_wxa_signature(session_key, raw_data, client_signature):
    """校验前端传来的rawData签名正确
    详情请参考
    https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/signature.html # noqa

    :param session_key: code换取的session_key
    :param raw_data: 前端拿到的rawData
    :param client_signature: 前端拿到的signature
    :raises: InvalidSignatureException
    :return: 返回数据dict
    """
    str2sign = (raw_data + session_key).encode("utf-8")
    signature = hashlib.sha1(str2sign).hexdigest()
    if signature != client_signature:
        from astar_wxpaysdk.exceptions import InvalidSignatureException
        raise InvalidSignatureException()


def to_text(value, encoding='utf-8'):
    """Convert value to unicode, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding='utf-8'):
    """Convert value to binary string, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return b''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return to_text(value).encode(encoding)


def timezone(zone):
    """Try to get timezone using pytz or python-dateutil

    :param zone: timezone str
    :return: timezone tzinfo or None
    """
    try:
        import pytz
        return pytz.timezone(zone)
    except ImportError:
        pass
    try:
        from dateutil.tz import gettz
        return gettz(zone)
    except ImportError:
        return None


def get_querystring(uri):
    """Get Querystring information from uri.

    :param uri: uri
    :return: querystring info or {}
    """
    parts = urlparse.urlsplit(uri)
    return urlparse.parse_qs(parts.query)


def byte2int(c):
    if six.PY2:
        return ord(c)
    return c
