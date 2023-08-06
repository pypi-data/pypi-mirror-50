# -*- coding:utf-8 -*-
from ucenter_base import UCenterBase
import json

class UCenterPermission(UCenterBase):
    def __init__(self, info_config):
        u"""
        :param info_config: type: Config
        """
        UCenterBase.__init__(self, info_config=info_config)

    def user_set_role(self, uid="", roles=None, app=""):
        u"""
        给用户设置角色
        :param uid: 用户id
        :param roles: 角色id列表
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/user')
        params = {"control_app": app}
        json_data = {

        }

        if uid:
            json_data['id'] = uid
        if roles is not None:
            json_data['roles'] = roles

        resp = self.request.post(url=uri, params=params, json=json_data)
        self.format_response(resp)

    def user_set_resource_scope(self, uid="", resources=None, scopes=None, app=""):
        u"""
        给用户添加角色
        :param uid: 用户id
        :param resources: 资源id列表
        :param scopes: scope范围列表
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/user')
        params = {"control_app": app}
        json_data = {
            "id": uid
        }
        if resources is not None:
            json_data['resources'] = resources
        if scopes is not None:
            json_data['scopes'] = scopes

        resp = self.request.post(url=uri, params=params, json=json_data)
        self.format_response(resp)

    def delete_userauth(self, uid="", app=""):
        u"""
        删除当前业务线与用户绑定关系
        :param uid: 用户id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/user')
        args = {"id": uid, "control_app": app}
        resp = self.request.delete(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['message']

    def add_userauth(self, uid="", resources=None, roles=None, scopes=None, app=""):
        u"""
        给用户添加角色
        :param uid: 用户id
        :param resources: 资源id列表
        :param scopes: scope范围列表
        :param roles: 角色id列表
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/user')
        params = {"control_app": app}
        json_data = {
            "id": uid,
            "resources": resources if resources else [],
            "roles": roles if roles else [],
            "scopes": scopes if scopes else []
        }
        resp = self.request.post(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['message']

    def role_set_resource_scope(self, scopes=None, id="", resources=None, app=""):
        u"""
        添加角色
        :param scopes: 资源作用范围
        :param id: 用户id
        :param resources: 资源
        :param app:属于哪个app
        :return:
        """

        uri = self.format_uri('/auth/role')
        params = {"control_app": app}
        json_data = {
            "id": id
        }
        if scopes is not None:
            json_data['scopes'] = scopes
        if resources is not None:
            json_data['resources'] = resources
        resp = self.request.put(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def get_user_auths(self, order_by="updateAt", page_num=1, page_size=10, resource="", role="", user_ids=None,
                       app=""):
        u"""
        获取分页 - 用户权限信息
        :param uid: 用户id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/users')
        params = {"order_by": order_by,
                  "page_num": page_num,
                  "page_size": page_size,
                  "resource": resource,
                  "role": role,
                  "control_app": app}
        json_data = {"user_ids": user_ids
                     }
        resp = self.request.post(url=uri, params=params, json=json_data)
        resp = self.format_response(resp)
        return resp['data']

    def get_user_and_auths(self, order_by="updateAt", page_num=1, page_size=10, resource="", role="", user_ids=None,
                       app=""):
        u"""
        获取分页 - 用户权限信息
        :param uid: 用户id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/userinfos')
        params = {"order_by": order_by,
                  "page_num": page_num,
                  "page_size": page_size,
                  "resource": resource,
                  "role": role,
                  "user_ids": user_ids,
                  "control_app": app}
        resp = self.request.get(url=uri, params=params)
        resp = self.format_response(resp)
        return resp['data']

    def get_user_auth(self, uid="", app=""):
        u"""
        获取用户的权限信息
        :param uid: 用户id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/user')
        params = {"id": uid, "control_app": app}
        resp = self.request.get(url=uri, params=params)
        resp = self.format_response(resp)
        return resp['data']

    def get_user_and_auth(self, uid="", app=""):
        u"""
        获取用户信息和其权限信息
        :param uid: 用户id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/userinfo')
        params = {"id": uid, "control_app": app}
        resp = self.request.get(url=uri, params=params)
        resp = self.format_response(resp)
        return resp['data']

    def user_get_control_apps(self, uid="", app=""):
        u"""
        获取指定的管理员用户可管理的apps
        :param uid:
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/useradmin')
        params = {"id": uid, "control_app": app}
        resp = self.request.get(url=uri, params=params)
        resp = self.format_response(resp)
        return resp['data']

    def role_add(self, scopes="", app="", attrs="", id="", resources="", desc=""):
        u"""
        添加角色
        :param scopes: 资源作用范围
        :param app: 角色所属应用名，必传
        :param attrs: 额外属性
        :param id: 角色id，例 /dpap/bjcancer/search
        :param resources: 资源
        :param desc: 描述，备注
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/role')
        params = {"control_app": app}
        json_data = {
            "scopes": scopes if scopes else [],
            "app": app,
            "attrs": json.dumps(attrs) if attrs else '{}',
            "id": id,
            "resources": resources if resources else [],
            "desc": desc
        }
        resp = self.request.post(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def role_put(self, scopes=None, attrs="", id="", resources=None, desc="", app=""):
        u"""
        添加角色
        :param scopes: 资源作用范围
        :param attrs: 额外属性
        :param id: 用户id
        :param resources: 资源
        :param desc: 描述，备注
        :param app:属于哪个app
        :return:
        """

        uri = self.format_uri('/auth/role')
        params = {"control_app": app}
        json_data = {
            "id": id
        }
        if scopes is not None:
            json_data['scopes'] = scopes
        if resources is not None:
            json_data['resources'] = resources
        if attrs:
            json_data['attrs'] = json.dumps(attrs)
        if desc:
            json_data['desc'] = desc

        resp = self.request.put(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def role_get(self, role_id, app=""):
        u"""
        获取角色详情
        :param role_id: 角色id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/role')
        args = {
            "id": role_id,
            "control_app": app
        }
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def role_del(self, role_id, app=""):
        u"""
        删除角色
        :param role_id: 角色id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/role')
        args = {
            "id": role_id,
            "control_app": app
        }
        resp = self.request.delete(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['message']

    # def roles_get(self, level=0, pid=""):
    #     u"""
    #     分层级获取角色列表。只能获取当前部署应用-集群的角色列表
    #     :param level:
    #     :param pid:
    #     :return:
    #     """
    #
    #     uri = self.format_uri('/auth/roles')
    #     args = {
    #         'level': level,
    #         'pid': pid
    #     }
    #     resp = self.request.get(uri, params=args)
    #     format_resp = self.format_response(resp)
    #     return format_resp['data']

    def resource_add(self, app="", attrs="", id="", desc=""):
        u"""
        添加资源
        :param app: 资源所属应用名，必传
        :param attrs: 额外属性
        :param id: 资源id，例 /dpap/bjcancer/search
        :param desc: 描述，备注
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/resources')
        params = {"control_app": app}
        json_data = {
            "app": app,
            "attrs": json.dumps(attrs) if attrs else '{}',
            "id": id,
            "desc": desc
        }
        resp = self.request.post(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def resource_put(self, attrs="", id="", desc="", app=""):
        u"""
        添加资源
        :param attrs: 额外属性
        :param id: 用户id
        :param desc: 描述，备注
        :param app:属于哪个app
        :return:
        """

        uri = self.format_uri('/auth/resource')
        params = {"control_app": app}
        json_data = {
            "id": id
        }
        if attrs:
            json_data['attrs'] = json.dumps(attrs)
        if desc:
            json_data['desc'] = desc

        resp = self.request.put(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def resource_get(self, resource_id="", app=""):
        u"""
        获取资源详情
        :param resource_id: 资源id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/resource')
        args = {
            "id": resource_id,
            'control_app': app
        }
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def resource_del(self, resource_id, app=""):
        u"""
        删除资源
        :param resource_id: 资源id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/resource')
        args = {
            "id": resource_id,
            "control_app": app
        }
        resp = self.request.delete(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['message']

    # def resources_get(self, level=0, pid=""):
    #     u"""
    #     分层级获取资源列表。只能获取当前部署应用-集群的资源列表
    #     :param level:
    #     :param pid:
    #     :return:
    #     """
    #
    #     uri = self.format_uri('/auth/resources')
    #     args = {
    #         'level': level,
    #         'pid': pid
    #     }
    #     resp = self.request.get(uri, params=args)
    #     format_resp = self.format_response(resp)
    #     return format_resp['data']

    def scope_add(self, name="", value="", resource="", app=""):
        u"""
        添加资源对应scope
        :param name: scope名，即key
        :param value: scope值， 即value
        :param resource: 资源id，例 /dpap/bjcancer/search
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/scope')
        params = {"control_app": app}
        json_data = {
            "name": name,
            "value": value,
            "resource": resource
        }
        resp = self.request.post(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def scope_put(self, name="", id="", value="", resource="", app=""):
        u"""
        修改资源对应scope
        :param id: scope id, 即scope id
        :param name: scope名，即key
        :param value: scope值， 即value
        :param resource: 资源id，例 /dpap/bjcancer/search
        :param app:属于哪个app
        :return:
        """

        uri = self.format_uri('/auth/scope')
        params = {"control_app": app}
        json_data = {
            "id": id
        }
        if name:
            json_data['name'] = name
        if value:
            json_data['value'] = value
        if resource:
            json_data['resources'] = resource

        resp = self.request.put(uri, params=params, json=json_data)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def scope_get(self, scope_id="", app=""):
        u"""
        获取scope 资源范围 id
        :param scope_id: scope id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/scope')
        args = {
            "id": scope_id,
            "control_app": app
        }
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['data']

    def scope_del(self, scope_id="", app=""):
        u"""
        删除scope 资源范围 id
        :param scope_id: scope id
        :param app:属于哪个app
        :return:
        """
        uri = self.format_uri('/auth/scope')
        args = {
            "id": scope_id,
            "control_app": app
        }
        resp = self.request.delete(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['message']

    def scopes_get(self, resource_id="", app=""):
        u"""
        获取某个资源下有哪些scopes 作用范围
        :param resource_id: resource_id
        :param app:属于哪个app
        :return:
        """

        uri = self.format_uri('/auth/scope')
        args = {
            "resource": resource_id,
            "control_app": app
        }
        resp = self.request.get(uri, params=args)
        format_resp = self.format_response(resp)
        return format_resp['data']
