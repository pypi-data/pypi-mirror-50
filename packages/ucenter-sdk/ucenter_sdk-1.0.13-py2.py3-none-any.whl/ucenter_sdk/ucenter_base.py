# -*- coding:utf-8 -*-
from config import Config
from code_base import ResultCode
from ucenter_oauth2 import OAuth2Handler
from request_wraper import RequestWrap
import logging


class UCenterBase:
    def __init__(self, info_config):
        u"""
        :param info_config: type: Config
        """
        self.info_config = info_config
        self._service_uri = info_config.service_uri  # type: Config
        self.oauth2 = OAuth2Handler(oauth2_service_name=info_config.oauth2_service_name,
                                    oauth2_req_args=info_config.oauth2_req_args,
                                    logger=info_config.logger,
                                    default_endpoint=info_config.oauth2_default_endpoint)
        self.logger = info_config.logger
        # status_exception: http status_code 值不是200时，是否抛出异常
        # code_exception: response content code 值不是0时，是否抛出异常
        self.status_exception = True
        self.code_exception = True
        self.request = RequestWrap(logger=self.logger)
        self.cluster = info_config.cluster

    @property
    def service_uri(self):
        # if self._service_uri:
        #     return self._service_uri
        # else:
        #     self._service_uri = self.info_config.endpoint()
        #     return self._service_uri
        return self.info_config.endpoint()  # always get from etcd

    def format_uri(self, uri, has_params=False):
        u"""
        构造完整的http访问地址，添加access_token
        :param uri: URI
        :param has_params: False - access_token是第一个参数
        :return:
        """
        if has_params:
            uri = str.format('%s%s&access_token=%s' % (self.service_uri, str(uri), self.oauth2.access_token()))
        else:
            uri = str.format('%s%s?access_token=%s' % (self.service_uri, str(uri), self.oauth2.access_token()))

        return uri

    def refresh_token(self):
        u"""
        强制刷新oauth token
        :return: token
        """
        return self.oauth2.refresh_token()

    def logger_level(self, level=logging.INFO):
        self.logger.setLevel(level)

    def format_response(self, resp):
        u"""
        检查http的response
        :param resp: http response
        :return: 格式化后的resp，dict like，包括：status_code，code，message，data
        """
        format_resp = {'status_code': resp.status_code}
        if resp.status_code == 200:
            format_resp['code'] = resp.json().get('code')
            format_resp['message'] = resp.json().get('message')
            format_resp['data'] = resp.json().get('data')
            if format_resp['code'] != 0:
                self.logger.info("请求成功，远端处理出现逻辑错误！code=%s, message=%s" % (str(format_resp['code']), format_resp['message'].encode('utf8')))
                if self.code_exception:
                    raise Exception([ResultCode.REMOTE_RESP_ERROR[0],
                                     ResultCode.REMOTE_RESP_ERROR[1] + ':' +
                                     str(format_resp['code']) + format_resp['message'].encode('utf8')])
        else:
            self.logger.info("请求失败！请求异常，返回码为 %s" % str(resp.text))
            if self.status_exception:
                raise Exception(ResultCode.result(ResultCode.REMOTE_CALL_ERROR, data=resp.text, ext_info=resp.url))
        return format_resp

