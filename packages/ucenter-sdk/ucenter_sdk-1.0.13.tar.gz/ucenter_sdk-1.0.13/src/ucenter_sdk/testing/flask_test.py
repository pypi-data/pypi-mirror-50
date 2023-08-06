# -*- coding:utf-8 -*-
import time
import datetime
from flask import Flask, request, g, jsonify, redirect, session
from user_agents import parse
from config import Config
from ucenter_info import UCenterInfo
from ucenter_permission import UCenterPermission
from commons import oauth2_client_info, authentication
from ucenter_cas import UcenterCAS
from tools import cipher

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

###########
# 通用配置 #
###########
# 应用名，应用必须在统一用户中心中有注册
# 如果是新应用，可以找管理员添加
# 本应用名，服务注册和被其他应用在etcd发现使用。sdk_test
app_name = 'sdk_test'

# logger
logger_name = 'my_logger'

# 对于任何第三方应用通过OAuth2授权，通过access_token访问本应用，
# OAuth2都会使用该应用在OAuth2中配置的JWT secret，来加密并生成access_token。所以解密时需要使用同样的secret
# skey 长度必须为16/24/32
skey = 'ucenter_sdk_secret_11111'

# 单点登录后，本域名下的cookie名。同时超时时间需要设置
session_name = 'sdk_session'
EXPIRED_DAYS = datetime.timedelta(days=1)
expiration = datetime.datetime.now() + EXPIRED_DAYS

############################################################
#  sdk_test 通过OAuth2访问 ucenter_info 和ucenter_permission #
############################################################

######################
# 配置OAuth2 endpoint #
######################
oauth2_service_name = 'uoauth2'
oauth2_uri = Config.get_service_uri(service_name=oauth2_service_name, default='http://localhost:5103')

#######################################
# 配置OAuth2的参数（调用 ucenter_info）  #
#######################################
# 应用间授权（OAUTH2）凭证
# 在统一用户中心中申请（由管理员添加）
# 如应用sdk_test需要访问应用ucenter_info的接口，需要申请OAuth2凭证，其中：
# client_id：是该凭证的id
# client_secret：是该凭证的秘钥
# scope：是应用ucenter_info的名称
# grant_type：由管理员设置。client_credentials表示可以直接通过client_id和client_secret来获取access_token
oauth2_req_args = {
    'client_id': 'sdk_test_call_info',  # type: str
    'client_secret': 'sdk_test_call_info_secret',
    'grant_type': 'client_credentials',
    'scope': 'ucenter_info',
}

# 要访问的应用名ucenter_info
info_service_name = 'uinfo'

# 要访问的应用的服务地址。默认不用传，可以通过服务注册发现（结合service_name）获得。因这里是本地测试，需要传
info_service_uri = Config.get_service_uri(service_name=info_service_name, default='http://localhost:5101')

info_config = Config(oauth2_service_name=oauth2_service_name,
                     oauth2_req_args=oauth2_req_args,
                     oauth2_default_endpoint=oauth2_uri,
                     app_name=app_name,
                     service_name=info_service_name,
                     logger_name=logger_name,
                     service_uri=info_service_uri)

ucenter_info = UCenterInfo(info_config=info_config)
ucenter_info.code_exception = False

#############################################
# 配置OAuth2的参数（调用 ucenter_permission）  #
#############################################
oauth2_req_args = {
    'client_id': 'sdk_test_call_permission',  # type: str
    'client_secret': 'sdk_test_call_permission_secret',
    'grant_type': 'client_credentials',
    'scope': 'ucenter_permission',
}

# 要访问的应用名ucenter_info
permission_service_name = 'ucenter_permission'

# 要访问的应用的服务地址。默认不用传，可以通过服务注册发现（结合service_name）获得。因这里是本地测试，需要传
permission_service_uri = Config.get_service_uri(service_name=permission_service_name, default='http://localhost:5102')

permission_config = Config(oauth2_service_name=oauth2_service_name,
                           oauth2_req_args=oauth2_req_args,
                           oauth2_default_endpoint=oauth2_uri,
                           app_name=app_name,
                           service_name=permission_service_name,
                           logger_name=logger_name,
                           service_uri=permission_service_uri)

ucenter_permission = UCenterPermission(info_config=permission_config)
ucenter_permission.code_exception = False

#######################################
# 配置CAS - 单点登录参数                 #
#######################################
# current_service_uri = Config.get_service_uri(service_name='sdk_test', default='http://localhost:5006')
# cas_client_login = current_service_uri + '/user/cas/login'
# cas_client_logout = current_service_uri + '/user/cas/logout'
# cas_client_success_url = current_service_uri + '/index.html'
# cas_server_url = info_service_uri + '/cas'

ucenter_cas = UcenterCAS(ucenter_info=ucenter_info, app_name=app_name)


@app.before_request
def before_request():
    g.start_time = time.time()
    u"""
     从session中获取user 信息
    """
    token_str = request.args.get('access_token')
    if token_str:
        g.oauth2_client = oauth2_client_info(token_str, skey, abort_401=True)

    cookie_str = request.cookies.get(session_name, None)
    if cookie_str:
        session_info = cipher.decryptJson(skey=skey, text=cookie_str)
        uid = session_info.get('id')
        user = ucenter_info.user_get(uid)
        g.user = user


@app.after_request
def after_request(response):
    if getattr(session, 'need_delete', None):
        response.delete_cookie(session_name)

    if getattr(session, 'need_update', None):
        response.set_cookie(session_name, session[session_name], expires=expiration)

    info_config.logger.info(str(request.url) + ' cost millisecond： ' + str((time.time() - g.start_time) * 1000))
    return response


#@app.errorhandler(Exception)
#def error_exception(error):
#    return jsonify({'error': error.args[0]})


def set_cookie(key, val, expiration):
    cookies = session.get('cookies', [])
    cookie = {'key': key, 'val': val, 'expires': expiration}
    cookies.append(cookie)
    session['cookies'] = cookies


def mark_login(uid, op_session=None):
    timestamp = int(int(round(time.time() * 1000)))
    if not op_session:
        session[session_name] = str(cipher.encryptJson(skey, {'id': uid, 'time': timestamp}))
    session.need_update = True


def mark_logout():
    session.need_delete = True


def parse_UA():
    user_agent = parse(request.user_agent.string)
    os = user_agent.os.family
    osver = user_agent.os.version_string
    device = user_agent.device.family
    browser = user_agent.browser.family
    browserver = user_agent.browser.version_string
    is_pc = user_agent.is_pc
    is_mobile = user_agent.is_mobile
    ip = request.remote_addr
    url = request.url
    agent_info = {'os': os, 'device': device, 'browser': browser, 'ip': ip, 'is_pc': is_pc, 'is_mobile': is_mobile}
    session['agent_info'] = agent_info
    #: 存储到g中，后面可能会从g中获取
    g.agent_info = agent_info
    # TODO: 其他定制化字段


@app.route('/ucenter_info/users/get')
@authentication(mode='LOGIN|OAUTH2', resource='/sdk_test/ucenter_info/users')
def ucenter_users_get():
    print('test')
    users = ucenter_info.users_get()
    return jsonify(users)


# http://localhost:5006/ucenter_info/users/get_by_name?name=super_admin
@app.route('/ucenter_info/users/get_by_name')
@authentication(mode='PERMISSION|OAUTH2', resource='/sdk_test/ucenter_info/users', permission='/sdk_test')
def ucenter_users_get_by_name():
    name = request.args.get('name', None)
    users = ucenter_info.users_get(username=name)
    return jsonify(users)


@app.route('/ucenter_info/apps/get')
@authentication(mode='LOGIN|OAUTH2', resource='/sdk_test/ucenter_info/apps/get')
def ucenter_apps_get():
    print('test')
    apps = ucenter_info.apps_get()
    return jsonify(apps)


@app.route('/ucenter_info/user_auth/get_by_id')
@authentication(mode='LOGIN|OAUTH2', resource='/sdk_test/ucenter_info')
def ucenter_user_auth_get():
    uid = request.args.get('uid', None)
    user = ucenter_info.user_get(ucenter_user_id=uid)
    if not user.get('id'):
        return 'user not exist!'
    user_auth = ucenter_permission.get_user_auth(uid=uid)
    user_apps = ucenter_permission.user_get_control_apps(uid=uid)
    return jsonify({'user': user, 'user_auth': user_auth, 'user_apps':user_apps})


@app.route('/test/ucenter_permission')
@authentication(mode='PERMISSION', permission='/sdk_test/test/ucenter_permission')
def test_permission_info():
    print('test')
    uid = g.user.get('id')
    roles = ucenter_permission.get_user_auth(uid)
    return jsonify(roles)


@app.route('/')
def hello_world():
    print('test')
    users = ucenter_info.cas_server_info()
    #users = ucenter_info.cas_client_info('ucenter_info')
    return jsonify(users)


@app.route('/user/cas/login', methods=['GET', 'POST'])
def cas_login():
    u"""
    CAS Login
    :return:
    """
    if getattr(g, 'user', None):
        return redirect(ucenter_cas.cas_client_success_url)
    [uid, redirect_url] = ucenter_cas.login()
    if uid:
        user = ucenter_info.user_get(ucenter_user_id=uid)
        if user:
            mark_login(user.get('id'))
            return redirect(redirect_url)
    else:
        return redirect(redirect_url)


@app.route('/user/cas/logout', methods=['GET', 'POST'])
def cas_logout():
    u"""
    CAS Login
    :return:
    """
    [status, redirect_url] = ucenter_cas.logout()
    if status:
        # cas server already logout, redirect_url is index.html
        mark_logout()
        return redirect(redirect_url)
    else:
        # cas server not logout, redirect_url is cas server logout
        return redirect(redirect_url)


@app.route('/index.html', methods=['GET'])
def index_page():
    user = getattr(g, 'user', None)
    if user:
        return jsonify(g.user)
    else:
        return 'not login!'


if __name__ == '__main__':
    app.run(debug=True, port=5006, host='0.0.0.0')
