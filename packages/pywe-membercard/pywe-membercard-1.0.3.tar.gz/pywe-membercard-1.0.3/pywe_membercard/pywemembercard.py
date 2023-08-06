# -*- coding: utf-8 -*-

from furl import furl
from pywe_card import card_create, card_update
from pywe_token import BaseToken, final_access_token


class MemberCard(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(MemberCard, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 8 管理会员卡, Refer: https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Manage_Member_Card.html
        # 8.1 拉取会员信息（积分查询）接口
        self.GET_USERINFO = self.API_DOMAIN + '/card/membercard/userinfo/get'
        # 卡券-小程序打通, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1499332673_Unm7V
        self.GET_ACTIVATE_URL = self.API_DOMAIN + '/card/membercard/activate/geturl'

    def create(self, data, appid=None, secret=None, token=None, storage=None):
        return card_create(data, appid=appid, secret=secret, token=token, storage=storage)

    def update(self, data, appid=None, secret=None, token=None, storage=None):
        return card_update(data, appid=appid, secret=secret, token=token, storage=storage)

    def get_userinfo(self, card_id, code, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.GET_USERINFO,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'card_id': card_id,
                'code': code,
            },
        )

    def get_activate_url(self, card_id, outer_str=None, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.GET_ACTIVATE_URL,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'card_id': card_id,
                'outer_str': outer_str,
            },
        )

    def get_miniapp_extraData(self, card_id, outer_str=None, appid=None, secret=None, token=None, storage=None):
        data = self.get_activate_url(card_id, outer_str=outer_str, appid=appid, secret=secret, token=token, storage=storage)
        url = data.get('url', '')
        if not url:
            return data
        return dict(furl(url).args)


membercard = MemberCard()
membercard_create = membercard.create
membercard_update = membercard.update
get_userinfo = membercard.get_userinfo
get_activate_url = membercard.get_activate_url
get_miniapp_extraData = membercard.get_miniapp_extraData
