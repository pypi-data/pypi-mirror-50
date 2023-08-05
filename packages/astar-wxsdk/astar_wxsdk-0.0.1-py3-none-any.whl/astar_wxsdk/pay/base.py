# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from astar_wxsdk.client.base import BaseWxAPI


class BaseWxPayAPI(BaseWxAPI):

    def _get(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, **kwargs)

    @property
    def app_id(self):
        return self._client.app_id

    @property
    def sub_app_id(self):
        return self._client.sub_app_id

    @property
    def mch_id(self):
        return self._client.mch_id

    @property
    def sub_mch_id(self):
        return self._client.sub_mch_id
