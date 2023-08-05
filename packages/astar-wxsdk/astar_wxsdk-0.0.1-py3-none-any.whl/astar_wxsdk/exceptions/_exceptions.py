#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: _exceptions.py
# @time: 2019/7/27 14:03
# @Software: PyCharm


__author__ = 'A.Star'

import six

from astar_wxsdk.utils import to_binary, to_text


# from astartool.string import to_binary, to_text

class WxException(Exception):
    """Base exception for wechatpy"""

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        _repr = 'Error code: {code}, message: {msg}'.format(
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def __repr__(self):
        _repr = '{klass}({code}, {msg})'.format(
            klass=self.__class__.__name__,
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


class WxClientException(WxException):
    """WeChat API client exception class"""

    def __init__(self, errcode, errmsg, client=None,
                 request=None, response=None):
        super(WxClientException, self).__init__(errcode, errmsg)
        self.client = client
        self.request = request
        self.response = response


class InvalidSignatureException(WxException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class APILimitedException(WxClientException):
    """WeChat API call limited exception class"""
    pass


class InvalidAppIdException(WxException):
    """Invalid app_id exception class"""

    def __init__(self, errcode=-40005, errmsg='Invalid AppId'):
        super(InvalidAppIdException, self).__init__(errcode, errmsg)


class WxOAuthException(WxClientException):
    """WeChat OAuth API exception class"""
    pass


class WxComponentOAuthException(WxClientException):
    """WeChat Component OAuth API exception class"""
    pass


class WxPayException(WxClientException):
    """WeChat Pay API exception class"""

    def __init__(self, return_code, result_code=None, return_msg=None,
                 errcode=None, errmsg=None, client=None,
                 request=None, response=None):
        """
        :param return_code: 返回状态码
        :param result_code: 业务结果
        :param return_msg: 返回信息
        :param errcode: 错误代码
        :param errmsg: 错误代码描述
        """
        super(WxPayException, self).__init__(
            errcode,
            errmsg,
            client,
            request,
            response
        )
        self.return_code = return_code
        self.result_code = result_code
        self.return_msg = return_msg

    def __str__(self):
        if six.PY2:
            return to_binary('Error code: {code}, message: {msg}. Pay Error code: {pay_code}, message: {pay_msg}'.format(
                code=self.return_code,
                msg=self.return_msg,
                pay_code=self.errcode,
                pay_msg=self.errmsg
            ))
        else:
            return to_text('Error code: {code}, message: {msg}. Pay Error code: {pay_code}, message: {pay_msg}'.format(
                code=self.return_code,
                msg=self.return_msg,
                pay_code=self.errcode,
                pay_msg=self.errmsg
            ))

    def __repr__(self):
        _repr = '{klass}({code}, {msg}). Pay({pay_code}, {pay_msg})'.format(
            klass=self.__class__.__name__,
            code=self.return_code,
            msg=self.return_msg,
            pay_code=self.errcode,
            pay_msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)
