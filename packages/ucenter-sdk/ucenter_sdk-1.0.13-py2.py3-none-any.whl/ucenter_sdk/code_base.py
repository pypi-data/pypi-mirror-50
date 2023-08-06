# -*- coding:utf-8 -*-


class ResultCode():
    def __init__(self):
        pass

    @staticmethod
    def result(result_code, data=None, ext_info=None):
        if not isinstance(result_code, list):
            raise Exception("result code type error")
        return {'code': result_code[0], 'message': result_code[1], 'data': data, 'ext_info': ext_info}

    SUCCESS_STATUS = 0
    SUCCESS = [SUCCESS_STATUS, 'success']

    # function status
    FUNCTION_STATUS = 100
    PHONE = FUNCTION_STATUS + 1
    EMAIL = FUNCTION_STATUS + 2
    USERID = FUNCTION_STATUS + 3
    USERNAME = FUNCTION_STATUS + 4
    UNKNOW = FUNCTION_STATUS + 5
    ADMIN = FUNCTION_STATUS + 6
    MYSELF = FUNCTION_STATUS + 7

    # login/session error
    LOGIN_ERROR = 200
    SINGLE_LOGIN_ERROR = [LOGIN_ERROR + 1, u'开放平台不允许多个客户端同时登陆']
    SESSION_NO_USER_ERROR = [LOGIN_ERROR + 2, u'当前session未绑定用户']
    OP_USER_NOT_EXIST = [LOGIN_ERROR + 3, u'开放平台不存在该用户']
    LOGIN_MULTI = [LOGIN_ERROR + 4, u'您当前已登录，不能重复登录']
    LOGIN_SUCCESS_USER_NOT_EXIST = [LOGIN_ERROR + 5, u'user=None. when set_session, user must exist!']
    LOGOUT_NOT_LOGIN = [LOGIN_ERROR + 6, u'您尚未登录']
    NOT_LOGIN = [LOGIN_ERROR + 7, u'您尚未登录']

    # user operation error
    USER_ERROR = 300
    REG_APPLY_INFO_NOT_EXIST = [USER_ERROR + 1, u'指定的用户注册申请信息不存在']
    APPROVED_NOT_ACCEPT = [USER_ERROR + 2, u'您尚未激活账号，请前往您申请的邮箱中点击激活链接，完成注册']
    REG_VALID_TOKEN_ERROR = [USER_ERROR + 3, u'token错误']
    ALREADY_ACTIVATE = [USER_ERROR + 4, u'无法重复激活（您已激活，请直接登录）']
    USER_ALREADY_DEV = [USER_ERROR + 5, u'用户已经是开发者，无须再申请']
    USER_ALREADY_OPENER = [USER_ERROR + 6, u'用户已经是开放者，无须再申请']
    ROLE_APPLY_INFO_NOT_EXIST = [USER_ERROR + 7, u'指定的权限申请信息不存在']
    NOT_ADMIN_NO_ACCESS = [USER_ERROR + 8, u'您不是管理员，没有权限访问该功能']
    NOT_DEVELOPER_NO_ACCESS = [USER_ERROR + 9, u'您不是开发者，没有权限访问该功能']
    NOT_OPENER_NO_ACCESS = [USER_ERROR + 10, u'您不是开放者，没有权限访问该功能']
    NOT_APPROVED_ACTIVATE = [USER_ERROR + 11, u'注册信息未通过，无法激活']
    ROLE_TYPE_ERROR = [USER_ERROR + 12, u'角色类型错误']
    ROLE_TYPE_EXIST = [USER_ERROR + 13, u'已拥有该角色']

    # notice error
    NOTICE_ERROR = 400
    NOTICE_NOT_EXIST = [NOTICE_ERROR + 1, u'指定的消息不存在']
    NOTICE_NOT_PERM = [NOTICE_ERROR + 2, u'您没有权限查看此消息']

    # Image error
    IMAGE_ERROR = 500
    IMAGE_NOT_EXIST = [NOTICE_ERROR + 1, u'指定的镜像不存在']
    IMAGE_NOT_PERM = [NOTICE_ERROR + 2, u'您没有权限查看此镜像']
    IMAGE_NOT_PERM_DEL = [NOTICE_ERROR + 3, u'您没有权限删除此镜像']

    # Image error
    DEPLOY_ERROR = 600
    DEPLOY_NOT_EXIST = [NOTICE_ERROR + 1, u'指定的部署信息不存在']
    DEPLOY_NOT_PERM = [NOTICE_ERROR + 2, u'您没有权限查看此部署信息']

    # Image error
    APP_ERROR = 700
    APP_NOT_EXIST = [NOTICE_ERROR + 1, u'指定的应用信息不存在']
    APP_NOT_PERM = [NOTICE_ERROR + 2, u'您没有权限查看此应用信息']
    APP_NOT_PERM_DEL = [NOTICE_ERROR + 2, u'您没有权限删除此应用信息']

    # 权限错误
    PERMISSION_ERROR = 800
    NO_PERMISSION_TO_ACCESS = [PERMISSION_ERROR + 1, u'没有权限']

    # open-platform error
    OP_ERROR = 1000
    EXCEPTION = [OP_ERROR + 1, u'内部错误']
    PARAM_ERROR = [OP_ERROR + 2, u'起始页超过总页数']
    OBJECT_ID_ERROR = [OP_ERROR + 3, u'不合法的id']
    PUT_PARAM_NO_EXT_FIELD = [OP_ERROR + 4, u'没有要更新的字段']
    REMOTE_CALL_ERROR = [OP_ERROR + 5, u'Remote Http Call Error!']
    REMOTE_RESP_ERROR = [OP_ERROR + 6, u'远端http服务返回code非0数据']
    RESULT_RESP_ERROR = [OP_ERROR + 7, u'result not dict response like']
    RESULT_CODE_ERROR = [OP_ERROR + 8, u'result not result code like']
    USER_REG_TYPE_ERROR = [OP_ERROR + 9, u'用户类型错误']

    # Type convert error
    CONVERT_ERROR = 11000
    DICT_CONVERT_TYPE_ERROR = [CONVERT_ERROR + 1, u'对象转换为dict类型是发生错误，不是string/unicode类型']
    DICT_CONVERT_CONTENT_ERROR = [CONVERT_ERROR + 2, u'对象转换为dict类型是发生错误，内容不是dict类型']
    STRING_CONVERT_ERROR = [CONVERT_ERROR + 3, u'对象转换为string类型是发生错误']
    PHONE_TYPE_ERROR = [CONVERT_ERROR + 4, u'电话的格式不正确']
    EMAIL_TYPE_ERROR = [CONVERT_ERROR + 5, u'邮箱的格式不正确']
    INT_TYPE_ERROR = [CONVERT_ERROR + 6, u'转换为整形错误']
