# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Author: 河北雪域网络科技有限公司 A.Star
# # @contact: astar@snowland.ltd
# # @site: www.snowland.ltd
# # @file: pay.py
# # @time: 2019/7/3 2:42
# # @Software: PyCharm
#
#
# __author__ = 'A.Star'
#
# # encoding: utf-8
#
# import time
#
# import requests
# from astartool.random import random_string
#
# from astar_wxpaysdk.account import WxPayAccount
# from astar_wxpaysdk.common import (
#     UFDODER_URL, WeChatcode, JSAPI_PARAMS_DEMO, REDIRECT_URL_PARAMS_DEMO, OPENID_PARAMS_DEMO
# )
# from astar_wxpaysdk.util import get_sign, trans_xml_to_dict, trans_dict_to_xml
#
#
# class WxPayUnifiedorde(WxPayAccount):
#     def wx_pay_unifiedorde(self, detail):
#         """
#         访问微信支付统一下单接口
#         :param detail:
#         :return:
#         """
#         detail['sign'] = get_sign(detail, self.access_key)
#         xml = trans_dict_to_xml(detail)  # 转换字典为XML
#         response = requests.post(UFDODER_URL, data=xml, verify=self.verify)  # 以POST方式向微信公众平台服务器发起请求
#         return response.content
#
#     def get_redirect_url(self, redirect_uri, response_type='code', scope='snsapi_base', state: str = None):
#         """
#         获取微信返回的重定向的url
#         :param redirect_uri: 设定重定向路由
#         :param response_type: 返回值类型, default: 'code'
#         :param scope: 获取信息类型，default:只获取基本信息
#         :param state: 自定义状态码
#         :return: url,其中携带code
#         """
#         urlinfo = REDIRECT_URL_PARAMS_DEMO.copy()
#         urlinfo['appid'] = self.app_id
#         urlinfo['redirect_uri'] = redirect_uri  # 设置重定向路由
#         urlinfo['response_type'] = response_type
#         urlinfo['scope'] = scope
#         urlinfo['state'] = state  # 自定义的状态码
#         info = requests.get(url=WeChatcode, params=urlinfo, verify=self.verify)
#         return info.url
#
#     def get_openid(self, code, state, state_check='mystate'):
#         """
#         获取微信的openid
#         :param code:
#         :param state:
#         :param state_check:
#         :return:
#         """
#         if WxPayUnifiedorde.check_code_and_state(code, state, state_check):
#             urlinfo = OPENID_PARAMS_DEMO.copy()
#             urlinfo['appid'] = self.app_id
#             urlinfo['secret'] = self.access_secret
#             urlinfo['code'] = code
#             urlinfo['grant_type'] = 'authorization_code'
#             info = requests.get(url=WeChatcode, params=urlinfo, verify=self.verify)
#             info_dict = eval(info.content.decode('utf-8'))
#             return info_dict['openid']
#         return None
#
#     def get_jsapi_params(self, openid, notify_url, description,
#                          total_fee=1, nonce_str=None, out_trade_no=None):
#         """
#         获取微信的Jsapi支付需要的参数
#         :param openid: 用户的openid
#         :param total_fee # 付款金额，单位是分，必须是整数
#         :param notify_url 回调的url
#         :param description 商品描述
#         :param nonce_str 验证串
#         :param out_trade_no 订单编号
#         :return:
#         """
#         params = JSAPI_PARAMS_DEMO.copy()
#         params = dict(params, **{
#             'appid': self.app_id,  # APPID
#             'mch_id': self.mch_id,  # 商户号
#             'nonce_str': nonce_str,
#             'out_trade_no': out_trade_no,  # 订单编号,可自定义
#             'total_fee': total_fee,  # 订单总金额
#             'spbill_create_ip': self.create_ip,  # 发送请求服务器的IP地址
#             'openid': openid,
#             'notify_url': notify_url,  # 支付成功后微信回调路由
#             'body': description,  # 商品描述
#         })
#         # 调用微信统一下单支付接口url
#         notify_result = self.wx_pay_unifiedorde(params)
#
#         params['sign'] = get_sign({
#             'appId': self.app_id,
#             "timeStamp": int(time.time()),
#             'nonceStr': random_string(16),
#             'package': 'prepay_id=' + trans_xml_to_dict(notify_result)['prepay_id'],
#             'signType': 'MD5',
#         }, self.access_key)
#         return params
#
#     @classmethod
#     def check_code_and_state(cls, code, state, state_check) -> bool:
#         """
#         :param code:
#         :param state:
#         :param state_check:
#         :return:
#         """
#         return code and state and state == state_check
#
#
# from wechatpy.utils import check_signature
# from wechatpy.exceptions import InvalidSignatureException
# from django.http import HttpResponse
# from wechatpy import parse_message, create_reply
# from wechatpy.replies import BaseReply
# from wechatpy import WeChatClient
# from wechatpy.oauth import WeChatOAuth
#
#
# import wx.wechat as wx_wechat
#
#
# # 23_nxUXZU935z5E--qZbxKd2YXc4cyRKwMyfGu0m3YB45CPXqIMw65rz-3WdrUJwRUWNEjrISYWl6908uG2F2ZNd8tAkIk3VK8qdwBBkFmJzBShbQzCi64kwTSutdwgF9jWfRW0r6cpcOGrHgRsUCJjABADLS",
#
#
#
# class WxPayAccount(WxClient):
#     """ 微信公众平台 OAuth 网页授权
#
#     详情请参考
#     https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419316505
#     """
#
#     API_BASE_URL = 'https://api.weixin.qq.com/'
#     OAUTH_BASE_URL = 'https://open.weixin.qq.com/connect/'
#
#     def __init__(self, app_id, secret, redirect_uri, scope='snsapi_base', state=''):
#         """
#
#         :param app_id: 微信公众号 app_id
#         :param secret: 微信公众号 secret
#         :param redirect_uri: OAuth2 redirect URI
#         :param scope: 可选，微信公众号 OAuth2 scope，默认为 ``snsapi_base``
#         :param state: 可选，微信公众号 OAuth2 state
#         """
#         self.app_id = app_id
#         self.secret = secret
#         self.redirect_uri = redirect_uri
#         self.scope = scope
#         self.state = state
#         self._http = requests.Session()
#
#     def _request(self, method, url_or_endpoint, **kwargs):
#         if not url_or_endpoint.startswith(('http://', 'https://')):
#             url = '{base}{endpoint}'.format(
#                 base=self.API_BASE_URL,
#                 endpoint=url_or_endpoint
#             )
#         else:
#             url = url_or_endpoint
#
#         if isinstance(kwargs.get('data', ''), dict):
#             body = json.dumps(kwargs['data'], ensure_ascii=False)
#             body = body.encode('utf-8')
#             kwargs['data'] = body
#
#         res = self._http.request(
#             method=method,
#             url=url,
#             **kwargs
#         )
#         try:
#             res.raise_for_status()
#         except requests.RequestException as reqe:
#             raise WxOAuthException(
#                 errcode=None,
#                 errmsg=None,
#                 client=self,
#                 request=reqe.request,
#                 response=reqe.response
#             )
#         result = json.loads(res.content.decode('utf-8', 'ignore'), strict=False)
#
#         if 'errcode' in result and result['errcode'] != 0:
#             errcode = result['errcode']
#             errmsg = result['errmsg']
#             raise WxOAuthException(
#                 errcode,
#                 errmsg,
#                 client=self,
#                 request=res.request,
#                 response=res
#             )
#
#         return result
#
#     def _get(self, url, **kwargs):
#         return self._request(
#             method='get',
#             url_or_endpoint=url,
#             **kwargs
#         )
#
#     @property
#     def authorize_url(self):
#         """获取授权跳转地址
#
#         :return: URL 地址
#         """
#         redirect_uri = quote(self.redirect_uri, safe=b'')
#         url_list = [
#             self.OAUTH_BASE_URL,
#             'oauth2/authorize?appid=',
#             self.app_id,
#             '&redirect_uri=',
#             redirect_uri,
#             '&response_type=code&scope=',
#             self.scope
#         ]
#         if self.state:
#             url_list.extend(['&state=', self.state])
#         url_list.append('#wechat_redirect')
#         return ''.join(url_list)
#
#     @property
#     def qrconnect_url(self):
#         """生成扫码登录地址
#
#         :return: URL 地址
#         """
#         redirect_uri = quote(self.redirect_uri, safe=b'')
#         url_list = [
#             self.OAUTH_BASE_URL,
#             'qrconnect?appid=',
#             self.app_id,
#             '&redirect_uri=',
#             redirect_uri,
#             '&response_type=code&scope=',
#             'snsapi_login'  # scope
#         ]
#         if self.state:
#             url_list.extend(['&state=', self.state])
#         url_list.append('#wechat_redirect')
#         return ''.join(url_list)
#
#     def fetch_access_token(self, code):
#         """获取 access_token
#
#         :param code: 授权完成跳转回来后 URL 中的 code 参数
#         :return: JSON 数据包
#         """
#         res = self._get(
#             'sns/oauth2/access_token',
#             params={
#                 'appid': self.app_id,
#                 'secret': self.secret,
#                 'code': code,
#                 'grant_type': 'authorization_code'
#             }
#         )
#         self.access_token = res['access_token']
#         self.open_id = res['openid']
#         self.refresh_token = res['refresh_token']
#         self.expires_in = res['expires_in']
#         return res
#
#     def refresh_access_token(self, refresh_token):
#         """刷新 access token
#
#         :param refresh_token: OAuth2 refresh token
#         :return: JSON 数据包
#         """
#         res = self._get(
#             'sns/oauth2/refresh_token',
#             params={
#                 'appid': self.app_id,
#                 'grant_type': 'refresh_token',
#                 'refresh_token': refresh_token
#             }
#         )
#         self.access_token = res['access_token']
#         self.open_id = res['openid']
#         self.refresh_token = res['refresh_token']
#         self.expires_in = res['expires_in']
#         return res
#
#     def get_user_info(self, openid=None, access_token=None, lang='zh_CN'):
#         """获取用户信息
#
#         :param openid: 可选，微信 openid，默认获取当前授权用户信息
#         :param access_token: 可选，access_token，默认使用当前授权用户的 access_token
#         :param lang: 可选，语言偏好, 默认为 ``zh_CN``
#         :return: JSON 数据包
#         """
#         openid = openid or self.open_id
#         access_token = access_token or self.access_token
#         return self._get(
#             'sns/userinfo',
#             params={
#                 'access_token': access_token,
#                 'openid': openid,
#                 'lang': lang
#             }
#         )
#
#     def check_access_token(self, openid=None, access_token=None):
#         """检查 access_token 有效性
#
#         :param openid: 可选，微信 openid，默认获取当前授权用户信息
#         :param access_token: 可选，access_token，默认使用当前授权用户的 access_token
#         :return: 有效返回 True，否则 False
#         """
#         openid = openid or self.open_id
#         access_token = access_token or self.access_token
#         res = self._get(
#             'sns/auth',
#             params={
#                 'access_token': access_token,
#                 'openid': openid
#             }
#         )
#         if res['errcode'] == 0:
#             return True
#         return False
