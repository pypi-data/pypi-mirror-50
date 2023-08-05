# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class BaseWxAPI(object):
    """ WeChat API base class """

    def __init__(self, client=None, verify=False):
        self._client = client
        self.API_BASE_URL = ''
        self.verify = verify

    def _get(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, **kwargs)

    @property
    def access_token(self):
        return self._client.access_token

    @property
    def session(self):
        return self._client.session

    @property
    def app_id(self):
        return self._client.app_id

    @property
    def app_secret(self):
        return self._client.app_secret
