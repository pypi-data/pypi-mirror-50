# -*- coding:utf-8 -*-
from config import Config
from ucenter_info import UCenterInfo
from ucenter_permission import UCenterPermission

####################
#  OAuth2 endpoint #
####################
oauth2_service_name = 'ucenter_oauth2'
oauth2_uri = Config.get_service_uri(service_name=oauth2_service_name, default='http://localhost:5103')

#######################################
# ucenter_permission 调用 ucenter_info #
#######################################
# 应用间授权（OAUTH2）凭证
# 在统一用户中心中申请（由管理员添加）
# 如应用A需要访问应用B的接口，需要申请OAuth2凭证，其中：
# client_id：是该凭证的id
# client_secret：是该凭证的秘钥
# scope：是应用B的名称
# grant_type：由管理员设置。client_credentials表示可以直接通过client_id和client_secret来获取access_token
oauth2_req_args = {
    'client_id': 'permission_call_info',  # type: str
    'client_secret': 'permission_call_info_secret',
    'grant_type': 'client_credentials',
    'scope': 'ucenter_info',
}

# 应用名，应用必须在统一用户中心中有注册
# 如果是新应用，可以找管理员添加
# ucenter_info
app_name = 'ucenter_info'

# 用于服务注册发现
service_name = 'ucenter_info'

# info service 地址。默认不传可以通过服务注册发现（结合service_name）获得
service_uri = Config.get_service_uri(service_name=service_name, default='http://localhost:5101')

# logger
logger_name = 'my_logger'

info_config = Config(oauth2_uri=oauth2_uri,
                     oauth2_req_args=oauth2_req_args,
                     app_name=app_name,
                     service_name=service_name,
                     logger_name=logger_name,
                     service_uri=service_uri)

ucenter_info = UCenterInfo(info_config=info_config)

#######################################
# ucenter_info 调用 ucenter_permission #
#######################################
# 应用间授权（OAUTH2）凭证
# 在统一用户中心中申请（由管理员添加）
oauth2_req_args = {
    'client_id': 'info_call_permission',  # type: str
    'client_secret': 'info_call_permission_secret',
    'grant_type': 'client_credentials',
    'scope': 'ucenter_permission',
}

# 应用名，应用必须在统一用户中心中有注册
# 如果是新应用，可以找管理员添加
# ucenter_info
app_name = 'ucenter_permission'

# 用于服务注册发现
service_name = 'ucenter_permission'

# service 地址。默认不传可以通过服务注册发现（结合service_name）获得
service_uri = 'http://localhost:5103'
service_uri = Config.get_service_uri(service_name=service_name, default='http://localhost:5101')

# logger
logger_name = 'my_logger'

permission_config = Config(oauth2_uri=oauth2_uri,
                           oauth2_req_args=oauth2_req_args,
                           app_name=app_name,
                           service_name=service_name,
                           logger_name=logger_name,
                           service_uri=service_uri)

ucenter_permission = UCenterPermission(info_config=info_config)


# TEST: users_get
users = ucenter_info.users_get()
for user in users['items']:
    print(user)


# TEST:
#roles = ucenter_permission.roles_get()
#for role in roles['items']:
#    print(role)

