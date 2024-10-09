# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :UserModel.py
# @Time      :2024/9/13 21:05
# @Author    :XiaoQi

import typing

from pydantic import Field
from sqlalchemy import Index, String, Integer, DateTime
from sqlalchemy.orm import mapped_column

from common.model.BaseModel import BaseModel
from common.utils.generate_rsa_key import decrypt_rsa_password

class User(BaseModel):
    id : int=Field(None,title="id",description="id")
    username: str = Field(..., title="用户名不能为空！", description='用户名')
    nickname: str = Field(..., title="用户昵称不能为空！", description='用户昵称')
    email: str = Field(None, description='邮箱')
    user_type: str = Field(None, description='用户类型')
    remarks: str = Field(None, description='用户描述')
    avatar: str = Field(None, description='头像')
    tags: typing.List = Field(None, description='标签')
    roles: typing.List = Field(None, description='权限')
    password: str = Field(description='标签', default=decrypt_rsa_password("123456"))


class UserUpdate(BaseModel):
    pass

class UserDelete(BaseModel):
    id: int = Field(None, title="id", description="id")

class UserQuery(BaseModel):
    username: str = Field(None, description='用户名')
    nickname: str = Field(None, description='昵称')
    user_ids: typing.List[int] = Field(None, description='用户id')

    class Config:
        from_attributes = True  # 是否使用orm模型(个人理解: 放行,不验证)


class UserLogin(BaseModel):
    username: str = Field(..., description='用户名')
    password: str = Field(..., description='密码')


class UserResetPwd(BaseModel):
    id: int = Field(..., description='用户id')
    old_pwd: str = Field(..., description='旧密码')
    new_pwd: str = Field(..., description='新密码')
    re_new_pwd: str = Field(..., description='二次输入新密码')


class UserLoginRecordIn(BaseModel):
    token: str = Field(None, description='token')
    code: str = Field(None, description="账号")
    user_id: int = Field(None, description="用户id")
    user_name: str = Field(None, description="用户名称")
    logout_type: str = Field(None, description="登出类型")
    login_type: str = Field(None, description="登录类型")
    login_time: str = Field(None, description="登录时间")
    logout_time: str = Field(None, description="登出时间")
    login_ip: str = Field(None, description="登录ip")
    ret_msg: str = Field(None, description="返回信息")
    ret_code: str = Field(None, description="返回code")
    address: str = Field(None, description="地址")
    source_type: str = Field(None, description="来源")


class UserLoginRecordQuery(BaseModel):
    token: str = Field(None, description='token')
    code: str = Field(None, description="账号")
    user_id: int = Field(None, description="用户id")
    user_name: str = Field(None, description="用户名称")
    logout_type: str = Field(None, description="登出类型")
    login_type: str = Field(None, description="登录类型")
    login_time: str = Field(None, description="登录时间")
    logout_time: str = Field(None, description="登出时间")
    login_ip: str = Field(None, description="登录ip")
    ret_msg: str = Field(None, description="返回信息")
    ret_code: str = Field(None, description="返回code")
    address: str = Field(None, description="地址")
    source_type: str = Field(None, description="来源")


class UserTokenIn(BaseModel):
    id: int = Field(None, description='id')
    token: str = Field(None, description='token')
    avatar: str = Field(None, description='头像')
    username: str = Field(None, description='用户名称')
    nickname: str = Field(None, description='用户昵称')
    roles: typing.List = Field(None, description='权限')
    tags: typing.List = Field(None, description='标签')
    login_time: str = Field(None, description='登录时间')
    login_ip: str = Field(None, description='登录ip')
    remarks: str = Field(None, description='备注')

class UserLoginRecordQuery(BaseModel):
    token: str = Field(None, description='token')
    code: str = Field(None, description="账号")
    user_id: int = Field(None, description="用户id")
    user_name: str = Field(None, description="用户名称")
    logout_type: str = Field(None, description="登出类型")
    login_type: str = Field(None, description="登录类型")
    login_time: str = Field(None, description="登录时间")
    logout_time: str = Field(None, description="登出时间")
    login_ip: str = Field(None, description="登录ip")
    ret_msg: str = Field(None, description="返回信息")
    ret_code: str = Field(None, description="返回code")
    address: str = Field(None, description="地址")
    source_type: str = Field(None, description="来源")


class UserIn(BaseModel):
    id: int = Field(None, title="id", description='id')
    username: str = Field(..., title="用户名不能为空！", description='用户名')
    nickname: str = Field(..., title="用户昵称不能为空！", description='用户昵称')
    email: str = Field(None, description='邮箱')
    user_type: str = Field(None, description='用户类型')
    remarks: str = Field(None, description='用户描述')
    avatar: str = Field(None, description='头像')
    tags: typing.List = Field(None, description='标签')
    roles: typing.List = Field(None, description='权限')
    password: str = Field(description='标签')