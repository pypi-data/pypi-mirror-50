# -*- coding:utf-8 -*-
from ucenter_base import UCenterBase


class UCenterInfo(UCenterBase):
    def __init__(self, info_config):
        u"""
        :param info_config: type: Config
        """
        UCenterBase.__init__(self, info_config=info_config)

    def user_add(self, json_data):
        u"""
        向用户中心添加用户
        :param json_data:
        :return:
        """
        uri = self.format_uri('/info/user')
        resp = self.request.post(uri, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def user_get(self, ucenter_user_id):
        u"""
        根据用户中心用户id，获取用户信息
        :param ucenter_user_id:
        :return:
        """
        uri = self.format_uri('/info/user/' + ucenter_user_id)
        resp = self.request.get(url=uri)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def user_del(self, ucenter_user_id):
        u"""
        删除用户中心的用户
        :param ucenter_user_id:
        :return:
        """
        uri = self.format_uri('/info/user/' + ucenter_user_id)
        resp = self.request.delete(url=uri)
        self.format_response(resp)

    def users_get(self, username=None, fullname=None, phone=None, email=None, app_id=None, cluster_id=None,
                  org_id=None, ids=None, page_num=1, page_size=10):
        u"""
        获取用户列表。默认参数None表示不对此条件进行过滤
        :param page_size:
        :param page_num:
        :param ids:
        :param app_id:
        :param username:
        :param fullname:
        :param phone:
        :param email:
        :param cluster_id:
        :param org_id:
        :return:
        """

        uri = self.format_uri('/info/user')
        args = {
            'order_by': 'createAt',
            'page_num': page_num,
            'page_size': page_size,
            'username': username,
            'fullname': fullname,
            'phone': phone,
            'email': email,
            'app': app_id,
            'cluster': cluster_id,
            'org': org_id,
            'ids': ids
        }
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def app_get(self, appid):
        u"""
        :param appid: app id, can not be empty
        :return: app data, dict like
        """
        uri = self.format_uri('/info/app/'+appid)
        resp = self.request.get(uri)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def app_add(self, json_data):
        u"""
        :param json_data:
        :return:
        """
        uri = self.format_uri('/info/app')
        resp = self.request.post(uri, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def app_del(self, appid):
        u"""
        :param appid:
        :return:
        """
        uri = self.format_uri('/info/app' + appid)
        resp = self.request.delete(uri)
        self.format_response(resp)

    def apps_get(self, page_num=1, page_size=10):
        args = {
            'order_by': 'createAt',
            'page_num': 1,
            'page_size': 10,
        }
        uri = self.format_uri('/info/app')
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        data = format_resp['data']
        return data

    def app_get_by_name(self, app_name):
        args = {
            'order_by': 'createAt',
            'page_num': 1,
            'page_size': 10,
            'name': app_name,
        }
        uri = self.format_uri('/info/app')
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        items = format_resp['data']['items']
        if items:
            return items[0]
        else:
            return {}

    def clusters_get(self, page_num=1, page_size=10):
        args = {
            'order_by': 'createAt',
            'page_num': 1,
            'page_size': 10,
        }
        uri = self.format_uri('/info/cluster')
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        data = format_resp['data']
        return data

    def clusters_get_by_name(self, cluster_name):
        args = {
            'order_by': 'createAt',
            'page_num': 1,
            'page_size': 10,
            'name': cluster_name,
        }
        uri = self.format_uri('/info/cluster')
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        items = format_resp['data']['items']
        if items:
            return items[0]
        else:
            return {}

    def login_check(self, login_name, password, captcha_id='', captcha_value='', use_captcha='0'):
        u"""
        :param login_name: 登录名，可以是用户名（本地库），手机号，邮箱，userid（带@+clusterid）
        :param password: 密码
        :param captcha_id:
        :param captcha_value:
        :param use_captcha: 是否使用验证码，默认不使用
        :return:
        """
        uri = self.format_uri('/passport/login/password/login')
        json_data = {'login_name': login_name,
                     'password': password,
                     'captchaid': captcha_id,
                     'captchavalue': captcha_value,
                     'usecaptcha': use_captcha,
                     }
        resp = self.request.post(uri, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def cas_server_info(self):
        u"""
        获取应用的cas 客户端信息
        :param app_name:
        :return:
        """
        uri = self.format_uri('/cas/server')
        resp = self.request.get(uri)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def cas_client_info(self, app_name, org):
        u"""
        获取应用的cas 客户端信息
        :param app_name:
        :return:
        """
        args = {
            'order_by': 'createAt',
            'page_num': 1,
            'page_size': 10,
            'app': app_name,
            "org": org
        }
        uri = self.format_uri('/cas/service')
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        items = format_resp['data']['items']
        if items:
            return items[0]
        else:
            return {}

