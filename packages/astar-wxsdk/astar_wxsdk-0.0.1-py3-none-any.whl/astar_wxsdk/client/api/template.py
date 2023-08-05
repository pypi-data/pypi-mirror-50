# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from astar_wxsdk.client.api.base import BaseWxAPI


class WxTemplate(BaseWxAPI):

    def set_industry(self, industry_id1, industry_id2):
        """
        设置所属行业
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277

        :param industry_id1: 公众号模板消息所属行业编号
        :param industry_id2: 公众号模板消息所属行业编号
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'template/api_set_industry',
            data={
                'industry_id1': industry_id1,
                'industry_id2': industry_id2
            },
            verify=self.verify
        )

    def get_industry(self):
        """
        获取设置的行业信息
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277

        :return: 返回的 JSON 数据包
        """
        return self._get(
            'template/get_industry',
            verify=self.verify
        )

    def get(self, template_id_short):
        """
        获得模板ID
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277

        :param template_id_short: 模板库中模板的编号，有“TM**”和“OPENTMTM**”等形式
        :return: 模板 ID
        """
        res = self._post(
            'template/api_add_template',
            data={
                'template_id_short': template_id_short
            },
            result_processor=lambda x: x['template_id'],
            verify=self.verify
        )
        return res

    add = get

    def get_all_private_template(self):
        """
        获取模板列表
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277

        :return: 返回的 JSON 数据包
        """
        return self._get(
            'template/get_all_private_template',
            verify=self.verify
        )

    def del_private_template(self, template_id):
        """
        删除模板
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277

        :param template_id: 公众帐号下模板消息ID
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'template/del_private_template',
            data={
                'template_id': template_id
            },
            verify=self.verify
        )
