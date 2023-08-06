# -*- encoding:utf-8 -*-
import os
import logging
import random


# TODO: Be aware that those envs strictly dependence with platform
KUBERNETES_PORT = os.environ.get('KUBERNETES_PORT', None)
PAAS_ETCD_ADDRS = os.environ.get('PAAS_ETCD_ADDRS', None)


class Config:
    def __init__(self,
                 oauth2_service_name,
                 oauth2_req_args,
                 oauth2_default_endpoint,
                 app_name,
                 service_name,
                 logger_name,
                 service_uri=None):
        self.oauth2_service_name = oauth2_service_name
        self.oauth2_req_args = oauth2_req_args
        self.oauth2_default_endpoint=oauth2_default_endpoint
        self.app_name = app_name
        self.service_name = service_name
        self.service_uri = service_uri
        self.cluster = self.get_cluster()
        self.logger = None
        self.logger = self.get_logger(logger_name)

    def endpoint(self):
        u"""
        设置用户中心地址
        :param uri:
        :return:
        """
        if KUBERNETES_PORT:
            return Config.get_k8s_service_uri(service_name=self.service_name)
        elif PAAS_ETCD_ADDRS:
            return Config.get_paas_service_uri(service_name=self.service_name)
        else:
            return self.service_uri

    @staticmethod
    def get_paas_service_uri(service_name):
        from archsdk import get_service
        service_endpoints = get_service(service_name=service_name)
        if service_endpoints:
            index = random.randint(0, len(service_endpoints) - 1)
            service_endpoint = service_endpoints[index]
            service_uri = str.format("http://%s:%s" % (str(service_endpoint['host']), str(service_endpoint['port'])))
        else:
            logging.error('service: ' + str(service_name) + ' not register!')
            service_uri = ''
        return service_uri

    @staticmethod
    def get_k8s_service_uri(service_name):
        return str.format("http://%s" % (str(service_name)))

    @staticmethod
    def get_service_uri(service_name, default=None):
        if KUBERNETES_PORT:
            return Config.get_k8s_service_uri(service_name=service_name)
        elif PAAS_ETCD_ADDRS:
            return Config.get_paas_service_uri(service_name=service_name)
        else:
            return default

    @staticmethod
    def register_service(service_name):
        pass
        #register(service_name=service_name)

    def client_credential(self, client_id, client_secret, grant_type, scope):
        u"""
        设置本应用在用户中心oauth2 server申请的客户端凭证
        :param client_id:
        :param client_secret:
        :param grant_type:
        :param scope:
        :return:
        """
        self.oauth2_req_args = {
            'client_id': client_id,  # type: str
            'client_secret': client_secret,
            'grant_type': grant_type,
            'scope': scope,
        }

    def get_logger(self, name):
        """　获取日志 logger """
        if self.logger:
            return self.logger

        # 1、创建一个logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # 2、创建一个handler，用于写入日志文件
        #fh = logging.FileHandler('test.log')
        #fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 3、定义handler的输出格式（formatter）
        # logging.basicConfig函数对日志的输出格式及方式做相关配置
        format_str='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        formatter = logging.Formatter(format_str)

        # 4、给handler添加formatter
        ch.setFormatter(formatter)

        # 5、给logger添加handler
        logger.addHandler(ch)
        self.logger = logger

        return self.logger

    def logger_level(self, level):
        self.logger.setLevel(level)

    @staticmethod
    def get_cluster():
        """　获取CLUSTER logger """
        if KUBERNETES_PORT:
            # TODO: K8S way to get cluster
            return 'K8S_CLUSTER'
        elif PAAS_ETCD_ADDRS:
            # TODO: Marathon way to get cluster
            return 'PAAS_CLUSTER'
        else:
            return 'LOCAL_CLUSTER'
