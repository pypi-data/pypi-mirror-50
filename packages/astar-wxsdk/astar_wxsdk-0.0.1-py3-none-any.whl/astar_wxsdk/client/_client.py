#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: _client.py
# @time: 2019/7/29 17:46
# @Software: PyCharm


__author__ = 'A.Star'
from astar_wxsdk.client.base import BaseWxClient
from astar_wxsdk.client import api


class WxClient(BaseWxClient):
    """
    微信 API 操作类
    通过这个类可以操作微信 API，发送主动消息、群发消息和创建自定义菜单等。
    """

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    card = api.WxCard()
    customservice = api.WxCustomService()
    datacube = api.WxDataCube()
    device = api.WxDevice()
    group = api.WxGroup()
    invoice = api.WxInvoice()
    jsapi = api.WxJSAPI()
    material = api.WxMaterial()
    media = api.WxMedia()
    menu = api.WxMenu()
    merchant = api.WxMerchant()
    message = api.WxMessage()
    misc = api.WxMisc()
    poi = api.WxPoi()
    qrcode = api.WxQRCode()
    scan = api.WxScan()
    semantic = api.WxSemantic()
    shakearound = api.WxShakeAround()
    tag = api.WxTag()
    template = api.WxTemplate()
    user = api.WxUser()
    wifi = api.WxWiFi()
    wxa = api.WxWxa()
    marketing = api.WxMarketing()

    def __init__(self, app_id, app_secret, access_token=None,
                 session=None, timeout=None, auto_retry=True, verify=False):
        super(WxClient, self).__init__(
            app_id,
            access_token,
            session,
            timeout,
            auto_retry,
            verify,
            app_secret=app_secret
        )

    def fetch_access_token(self):
        """
        获取 access token
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        return self._fetch_access_token(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.app_id,
                'secret': self.app_secret
            }, verify=self.verify
        )
