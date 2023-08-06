# -*- coding:utf-8 -*-
from flask import request
from cas_client import CASClient
from tools.popenapi import MYOPENAPI
import os
import random

TARGET = os.environ["PAAS_TARGET"]


def get_inner_server_url():
    if os.environ.get("PAAS_ETCD_ADDRS"):
        from archsdk import get_service
        service_endpoints = get_service("inf-arch-ucenter-info")
        index = random.randint(0, len(service_endpoints) - 1)
        service_endpoint = service_endpoints[index]
        return str.format("http://%s:%s" % (str(service_endpoint['host']), str(service_endpoint['port']))) + "/cas"
    elif os.environ.get("KUBERNETES_PORT"):
        return "http://inf-arch-ucenter-info/cas"


class NewCASClient(CASClient):

    def __init__(self,
                 server_url,
                 service_url=None,
                 auth_prefix='/cas',
                 proxy_url=None,
                 proxy_callback=None,
                 verify_certificates=False,
                 session_storage_adapter=None,
                 headers=None):
        super(NewCASClient, self).__init__(server_url,
                                           service_url,
                                           auth_prefix,
                                           proxy_url,
                                           proxy_callback,
                                           verify_certificates,
                                           session_storage_adapter,
                                           headers)
        self._interface = "http://openapi.intra.yiducloud.cn"
        self.new_server = get_inner_server_url()

    def _get_service_validate_url(self, ticket, service_url=None):
        template = '{server_url}{auth_prefix}/serviceValidate?'
        template += 'ticket={ticket}&service={service_url}'
        url = template.format(
            auth_prefix=self.auth_prefix,
            server_url=self.new_server if ".yiducloud.cn" not in self.server_url else \
                  self._interface + "/%s/%s/ucenter/uinfo/cas" % (os.environ.get("CENTER_CLUSTER", "bj"), TARGET),
            service_url=service_url or self.service_url,
            ticket=ticket,
        )
        if self.proxy_url:
            url = '{url}&pgtUrl={proxy_url}'.format(url, self.proxy_url)
        return url




class UcenterCAS():
    def __init__(self, ucenter_info, app_name, org):
        self.app_name = app_name
        self.ucenter_info = ucenter_info
        # 客户端登录地址。是后端的接口，负责跳转到server login并负责解析和校验从server返回的ST
        self.cas_client_login = None
        self.cas_client_logout = None
        # 如果登录成功，客户端要跳转的地址
        self._cas_client_success_url = None
        # server端点，主要有login和serviceValidate
        self.cas_server_url = None
        # client info get from ucenter cas server
        self.cas_client_info = {}
        self.cas_client = None
        self.org = org

    def cas_init(self):
        # TODO : 可能需要每次都获取
        self.cas_client_info = self.ucenter_info.cas_client_info(self.app_name, self.org)
        # 客户端登录地址。是后端的接口，负责跳转到server login并负责解析和校验从server返回的ST
        self.cas_client_login = str(self.cas_client_info.get('pattern', ''))
        self.cas_client_logout = str(self.cas_client_info.get('logout_callback', ''))
        # 如果登录成功，客户端要跳转的地址
        self.cas_client_success_url = str(self.cas_client_info.get('success_index', ''))
        # server端点，主要有login和serviceValidate
        self.cas_server_url = str(self.cas_client_info.get("server"))
        self.cas_client = NewCASClient(self.cas_server_url, auth_prefix='')

    # this field will be directly access, so we use property
    @property
    def cas_client_success_url(self):
        if not self._cas_client_success_url:
            self.cas_init()
        return self._cas_client_success_url

    @cas_client_success_url.setter
    def cas_client_success_url(self, val):
        self._cas_client_success_url = val

    def login(self):
        self.cas_init()

        ticket = request.args.get('ticket')
        # print(ticket)
        if ticket:
            cas_response = self.cas_client.perform_service_validate(
                ticket=ticket,
                service_url=self.cas_client_login,
                headers=MYOPENAPI.getOpenapiHeaders()
            )
            if cas_response and cas_response.success:
                uid = str(cas_response.data['id'])
                return [uid, self.cas_client_success_url]
        login_url = self.cas_client.get_login_url(service_url=self.cas_client_login)
        return [None, login_url]

    def logout(self):
        self.cas_init()

        status = request.args.get('status')
        if status:
            # cas server logout 返回
            return [status, self.cas_client_success_url]
        else:
            # local logout called, need to call cas server logout first
            logout_uri = self.cas_client.get_logout_url(service_url=self.cas_client_login)
            return [None, logout_uri]
