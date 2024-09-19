# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :BaseException.py
# @Time      :2024/9/12 21:21
# @Author    :XiaoQi


import  typing

from common.enum.code_enum import CodeEnum


class BaseException(Exception):
    def __init__(self,err_or_code: typing.Union[CodeEnum, str]):
        if isinstance(err_or_code, CodeEnum):
            code = err_or_code.code
            msg = err_or_code.msg
        else:
            code = CodeEnum.PARTNER_CODE_FAIL.code
            msg = err_or_code
        self.code = code
        self.msg = msg
    
    def __str__(self):
        return f"{self.code}:{self.msg}"

    def __repr__(self):
        return f"{self.code}:{self.msg}"
    
class IpError(BaseException):
    """ ip错误 """

    def __init__(self):
        super(IpError, self).__init__("ip 错误")


class SetRedis(BaseException):
    """ Redis存储失败 """

    def __init__(self):
        super(SetRedis, self).__init__("Redis存储失败")


class IdNotExist(BaseException):
    """ 查询id不存在 """

    def __init__(self):
        super(IdNotExist, self).__init__("查询id不存在")


class UserNotExist(BaseException):
    """ 用户不存在 """

    def __init__(self):
        super(UserNotExist, self).__init__("用户不存在")


class AccessTokenFail(BaseException):
    """ 访问令牌失败 """

    def __init__(self):
        super(AccessTokenFail, self).__init__(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL)


class ErrorUser(BaseException):
    """ 错误的用户名或密码 """

    def __init__(self):
        super(ErrorUser, self).__init__("错误的用户名或密码")


class PermissionNotEnough(BaseException):
    """ 权限不足,拒绝访问 """

    def __init__(self):
        super(PermissionNotEnough, self).__init__("权限不足,拒绝访问")


class ParameterError(BaseException):
    """ 参数错误 """

    def __init__(self, err_code: typing.Union[CodeEnum, str]):
        super(ParameterError, self).__init__(err_code)


class EnvConfInitError(BaseException):
    """ 环境配置初始化失败 """

    def __init__(self, err_code: typing.Union[CodeEnum, str]):
        super(EnvConfInitError, self).__init__(err_code)