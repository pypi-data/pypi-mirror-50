# -*- coding:utf-8 -*-
import logging
import datetime
from request_wraper import RequestWrap
from config import Config


class OAuth2Handler:
    # oauth2 endpoint
    def __init__(self, oauth2_service_name, oauth2_req_args, logger=None, default_endpoint=''):
        self.service_name = oauth2_service_name
        self.default_endpoint = default_endpoint
        self._token_endpoint = None
        # access_token
        self.token = None
        # 多少秒后过期
        self.expires_second = 0
        # 过期时间（预留180秒的时间窗口，既比oauth2指定的过期时间少180）。一旦过期，会重新获取access_token
        self.expires = datetime.datetime.now() + datetime.timedelta(seconds=self.expires_second-180)
        self.oauth2_req_args = oauth2_req_args
        self.request = RequestWrap(logger)
        if not logger:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
        self.token = None

    @property
    def token_endpoint(self):
        if self._token_endpoint:
            return self._token_endpoint
        else:
            self._token_endpoint = Config.get_service_uri(service_name=self.service_name, default=self.default_endpoint)
            if self._token_endpoint:
                self._token_endpoint += '/oauth/token'
                return self._token_endpoint
            else:
                self.logger.error('-------- OAuth2 service not register! --------')
                return ''

    def access_token(self, refresh=False):
        u"""
        获取access_token
        :param refresh: 是否强制刷新token
        :return:
        """
        # 刷新access_token
        if refresh:
            self.token = None
        # 已获取的token_token是否过期
        if self.token and datetime.datetime.now() < self.expires:
            return self.token
        else:
            resp = self.request.get(self.token_endpoint, params=self.oauth2_req_args)
            # 如果OAuth2 server 返回非200，（这里可以判断-1）则重新获取OAuth2地址，再尝试获取access_token
            if resp.status_code != 200:
                self.logger.error("1. Get OAuth2 AccessToken error! Error info is - " + resp.text)
                self._token_endpoint = None
                resp = self.request.get(self.token_endpoint, params=self.oauth2_req_args)
                if resp.status_code != 200:
                    self.logger.error("2. Get Latest Oauth2 service endpoint, and retry failed. Error info is -" + resp.text)
                    return None
                self.logger.error("2. Get Latest Oauth2 service endpoint, and retry success.")
            json = resp.json()
            self.token = str(json.get('access_token'))
            self.expires_second = json.get('expires_in')
            self.expires = datetime.datetime.now() + datetime.timedelta(seconds=self.expires_second-180)
            return self.token

    def refresh_token(self):
        u"""
        强制刷新oauth token
        :return: token
        """
        self.logger.info("refresh_token called")
        return self.access_token(refresh=True)

