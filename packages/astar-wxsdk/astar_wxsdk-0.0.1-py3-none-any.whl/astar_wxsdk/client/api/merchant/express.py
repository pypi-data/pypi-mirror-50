# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from astar_wxsdk.client.api.base import BaseWxAPI


class MerchantExpress(BaseWxAPI):

    API_BASE_URL = 'https://api.weixin.qq.com/'

    def add(self, delivery_template):
        return self._post(
            'merchant/express/add',
            data={
                'delivery_template': delivery_template
            }, verify=self.verify
        )

    def delete(self, template_id):
        return self._post(
            'merchant/express/del',
            data={
                'template_id': template_id
            }, verify=self.verify
        )

    def update(self, template_id, delivery_template):
        return self._post(
            'merchant/express/update',
            data={
                'template_id': template_id,
                'delivery_template': delivery_template
            }, verify=self.verify
        )

    def get(self, template_id):
        res = self._post(
            'merchant/express/getbyid',
            data={
                'template_id': template_id
            },
            result_processor=lambda x: x['template_info'],
            verify=self.verify
        )
        return res

    def get_all(self):
        res = self._get(
            'merchant/express/getall',
            result_processor=lambda x: x['template_info'],
            verify=self.verify
        )
        return res
