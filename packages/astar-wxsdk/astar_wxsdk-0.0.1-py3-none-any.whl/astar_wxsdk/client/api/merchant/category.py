# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from astar_wxsdk.client.api.base import BaseWxAPI


class MerchantCategory(BaseWxAPI):

    API_BASE_URL = 'https://api.weixin.qq.com/'

    def get_sub_categories(self, cate_id):
        res = self._post(
            'merchant/category/getsub',
            data={'cate_id': cate_id},
            result_processor=lambda x: x['cate_list'],
            verify=self.verify
        )
        return res

    def get_sku_list(self, cate_id):
        res = self._post(
            'merchant/category/getsku',
            data={'cate_id': cate_id},
            result_processor=lambda x: x['sku_table'],
            verify=self.verify
        )
        return res

    def get_properties(self, cate_id):
        res = self._post(
            'merchant/category/getproperty',
            data={'cate_id': cate_id},
            result_processor=lambda x: x['properties'],
            verify=self.verify
        )
        return res
