# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from astar_wxsdk.client.api.base import BaseWxAPI


class MerchantCommon(BaseWxAPI):

    API_BASE_URL = 'https://api.weixin.qq.com/'

    def upload_image(self, filename, image_data):
        res = self._post(
            'merchant/common/upload_img',
            params={
                'filename': filename
            },
            data=image_data,
            result_processor=lambda x: x['image_url'],
            verify=self.verify
        )
        return res
