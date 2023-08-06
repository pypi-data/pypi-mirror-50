# -*- coding:utf-8 -*-
import requests
import logging


class OpenAPI(object):
    def __init__(self):
        self.host = "http://openapi.intra.yiducloud.cn"
        self.__token = None
        self.__token_expire = None
        self.logger = logging.getLogger('passport.popenapi')
        self.__mailinterface = "http://openapi.intra.yiducloud.cn/opsrv/prod/mailserver/v1/mail"
        self.__smsInterface = "http://openapi.intra.yiducloud.cn/opsrv/prod/smsserver/v1/sms"
        self.__idtoken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVjZW50ZXIiLCJzY29wZXMiOlsib3BlbmFwaSJdLCJleHBpcmUiOjE1Mzk1ODk5NTUsImF1ZCI6Im9wZW5hcGkuaW50cmEueWlkdWNsb3VkLmNuIiwiZXhwIjoxNTM5NTg5OTU1LCJpc3MiOiJ5aWR1Y2xvdWQuY24iLCJpYXQiOjE1Mzg5ODUxNTUsInN1YiI6ImlkVG9rZW4ifQ.mD-ycHSFD--bbYTtv7pnIXD_-hBde03EcwMGpthNp9c"

    def url(self, uri):
        return "%s/openapi/%s" % (self.host, uri)

    def getOpenApiUrl(self, cluster, target, uri):
        """
        获得私有云openapi地址
        """
        return "%s/%s/%s/%s" % (self.host, cluster, target, uri)

    def getRelayApiUrl(self, uri, target="prod"):
        if target is None:
            target = "preview"
        return self.getOpenApiUrl("relay", target, uri)

    def getOpenapiHeaders(self):
        token = self.getRelayToken()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % token,
        }
        return headers

    def getRelayToken(self):
        # token每次使用重新获取
        url = self.url("idtoken/refresh")
        params = {"token": self.__idtoken}
        response = requests.post(url, data=params)
        if response.status_code != 200:
            return None
        self.__token = response.json().get("value")

        return self.__token


MYOPENAPI = OpenAPI()
