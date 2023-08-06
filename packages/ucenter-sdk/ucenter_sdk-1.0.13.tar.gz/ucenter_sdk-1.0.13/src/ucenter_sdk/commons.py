# -*- coding:utf-8 -*-
from flask import g, abort
from functools import wraps
from code_base import ResultCode
from datetime import datetime, timedelta
import jwt


###############
#  鉴权相关    #
###############
def authentication(mode='LOGIN',
                   permission=None,
                   role=None,
                   resource=None,
                   scopes=None,
                   auth_fail_handler=None
                   ):
    u"""
    接口鉴权
    :param mode: 鉴权模式。
                 'LOGIN' - 用户需要登录；
                 'PERMISSION' - 需要验证用户的权限，具体需要验证哪个权限，由后面的permission字段指明；
                 'ROLE' - 需要验证用户的角色，具体需要验证哪个角色，由后面的role字段指明；
                 'OAUTH2' - 需要验证OAUTH2，具体需要验证哪个resource，由后面resource字段指明；
    :param permission: 需要验证的权限
                       1. 如果是str，则需要验证当前用户要有该permission或该permission的父permission（前缀匹配）
                       2. 如果是dict，则dict的可以为需要验证的permission，value为需要验证的scope
    :param role: 需要验证的角色。要验证该用户有该role或者该role的父role（前缀匹配）
    :param resource: 需要验证的resource（在OAUTH2授权管理系统中，给其他应用授权时指定的resource）。
    :param auth_fail_handler: 验证失败的处理函数；
    :param scopes: 与permission鉴权模式配合使用
    :return: True（鉴权成功）/False（鉴权失败）
    """

    def wrapper(view_function):
        @wraps(view_function)
        def decorator(*args, **kwargs):
            status = authentication_func(mode, permission, role, resource, scopes)
            if status:
                return view_function(*args, **kwargs)
            else:
                if not auth_fail_handler:
                    if 'LOGIN' in mode.split('|'):
                        '''
                        Receiving a 401 response is the server telling you, “you aren’t authenticated, either not 
                        authenticated at all or authenticated incorrectly–but please re-authenticate and try again.”
                        '''
                        abort(401, {'code': ResultCode.NOT_LOGIN[0],
                                    'data': "You have NO PERMISSION to access this API since you are NOT LOGIN!"})
                    else:
                        '''
                        Receiving a 403 response is the server telling you, “I’m sorry. I know who you are and 
                        I believe who you say you are, but you just don’t have permission to access this resource. 
                        Maybe if you ask the system administrator, you’ll get permission. 
                        But please don’t bother me again until you get the permission.”
                        '''
                        abort(403, {'code': ResultCode.NO_PERMISSION_TO_ACCESS[0],
                                    'data': "You have NO PERMISSION to access this API, make sure you got the right "
                                            "permission from system administrator!"})
                else:
                    return auth_fail_handler()
        return decorator

    return wrapper


def authentication_login():
    user = getattr(g, 'user', None)
    if not user:
        return False
    else:
        return True


def authentication_permission(permission, scopes=None):
    u"""
    permission鉴权方式：
    1. 如果permission为空，无权限
    2. 如果当前用户是未登录状态，无权限
    3. 如果当前登录用户的permission为空，无权限
    4. 如果用户拥有的权限之一是参数权限的父类，有权限，
    5. 如果用户拥有的权限和参数权限一致，则
       a. 如果参数scopes为空，有权限
       b. 如果参数scopes是用户拥有的scopes的子集，有权限
       c. 其他情况，无权限
    :param permission:
    :param scopes:
    :return:
    """
    # 1
    if not permission:
        return False

    user = getattr(g, 'user', None)
    # 2
    if not user:
        return False

    user_permissions = user.get('permissions', None)
    # 3
    if not user_permissions:
        return False

    user_scopes = user.get('scopes', {})
    for key in user_permissions:
        if has_prefix(key, permission):
            # 4
            if key != permission:
                return True
            else:
                # 5.a
                if not scopes:
                    return True
                # 5.b
                if set(scopes.items()).issubset(user_scopes.items()):
                    return True
                # 5.c
                else:
                    continue
    return False


def authentication_role(role):
    if not role:
        return False

    user = getattr(g, 'user', None)
    if not user:
        return False

    roles = user.get('roles', None)
    if not roles:
        return roles

    for key in roles:
        if has_prefix(key, role):
            return True
    return False


def authentication_oauth2(resource):
    client = getattr(g, 'oauth2_client', None)
    if not client:
        return False
    if not resource:  # 只要是access_token合法，就允许访问
        return True
    resources = eval(client.get('resources'))
    for key in resources.keys():
        if has_prefix(key, resource):
            return True
    return False


def authentication_func(mode='LOGIN',
                        permission=None,
                        role=None,
                        resource=None,
                        scopes=None
                        ):
    u"""
    接口鉴权
    :param mode: 鉴权模式。
                 'LOGIN' - 用户需要登录；
                 'PERMISSION' - 需要验证用户的权限，具体需要验证哪个权限，由后面的permission字段指明；
                 'ROLE' - 需要验证用户的角色，具体需要验证哪个角色，由后面的role字段指明；
                 'OAUTH2' - 需要验证OAUTH2，具体需要验证哪个resource，由后面resource字段指明；
    :param permission: 需要验证的权限
                       1. 如果是str，则需要验证当前用户要有该permission或该permission的父permission（前缀匹配）
                       2. 如果是dict，则dict的key为需要验证的permission，value为需要验证的scope
    :param role: 需要验证的角色。要验证该用户有该role或者该role的父role（前缀匹配）
    :param resource: 需要验证的resource（在OAUTH2授权管理系统中，给其他应用授权时指定的resource）。
    :param scopes:
    :return: True（鉴权成功）/False（鉴权失败）
    """
    modes = mode.split('|')
    for m in modes:
        if m == 'LOGIN':
            if authentication_login():
                return True
        elif m == 'OAUTH2':
            if authentication_oauth2(resource):
                return True
        elif m == 'PERMISSION':
            if authentication_permission(permission, scopes):
                return True
        elif m == 'ROLE':
            if authentication_role(role):
                return True
    return False


def has_prefix(prefix, find_str):
    u"""
    给定前缀字符转和目标字符串，判断目标字符串中是否包含前缀字符串
    用于判断对于给定的一个权限/角色是否包含指定的权限
    如：给定/app1/cluster1/xxx1，判断其是否是指定的字符串/app1/cluster1/xxx1/zzz2的父级
    :param prefix:
    :param find_str:
    :return:
    """
    # 如果prefix与
    if prefix == find_str:
        return True
    elif find_str.startswith(prefix + '/'):
        return True
    else:
        return False


class JwtToken:
    @staticmethod
    def encode_token(info, skey):
        """
        生成认证Token
        :param skey:
        :return: string
        """
        try:

            headers = {
                "typ": "JWT",
                "alg": "HS256",
            }

            payload = {
                'exp': datetime.utcnow() + timedelta(days=10),  # 这里不验证时间，该jwt token在数据库中有过期时间
                'iat': datetime.utcnow(),
                'iss': 'ucenter',
                'headers': headers,
                "info": str(info)
            }
            return jwt.encode(
                payload,
                skey,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token, skey):
        """
        验证Token
        :param skey:
        :param token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(token, skey, options={'verify_exp': True})
            if 'headers' in payload and 'info' in payload:
                return payload
            else:
                return "Token信息格式错误"
        except jwt.ExpiredSignatureError:
            return "Token过期"
        except jwt.InvalidTokenError:
            return "无效的Token"


def oauth2_client_info(token_str, skey, abort_401=False):
    # 授权的用户和app必须在当前用户中心数据库中有存储
    try:
        info = JwtToken.decode_auth_token(token_str, skey).get('info')
    except Exception as e:
        if abort_401:
            abort(401, {'code': ResultCode.NO_PERMISSION_TO_ACCESS[0],
                        'data': "access_token invalid"})
        else:
            raise Exception("access_token invalid")
    client_info = eval(info)
    return client_info

