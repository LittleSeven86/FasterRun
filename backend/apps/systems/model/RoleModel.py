# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :RoleModel.py
# @Time      :2024/9/12 21:48
# @Author    :XiaoQi
import typing

from pydantic import Field
from common.model.BaseModel import BaseModel


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