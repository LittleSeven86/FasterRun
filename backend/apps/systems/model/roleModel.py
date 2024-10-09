# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :roleModel.py
# @Time      :2024/9/22 15:57
# @Author    :XiaoQi
import typing


from common.model.BaseModel import BaseModel

from pydantic import Field, root_validator


class RoleIn(BaseModel):
    id: int = Field(None, description="角色id")
    name: str = Field(..., description="角色名称")
    role_type: int = Field(default=10, description="角色类型")
    menus: str = Field(..., description="菜单列表")
    description: str = Field(None, description="描述")
    status: int = Field(default=10, description="状态 10 启用 20 禁用")

    @root_validator(pre=True)
    def root_validator(cls, data: typing.Dict[typing.Text, typing.Any]):
        menus = data.get("menus", [])
        if menus:
            data["menus"] = ','.join(list(map(str, menus)))
        return data


class RoleQuery(BaseModel):
    id: int = Field(None, description="角色id")
    name: str = Field(None, description="角色名称")
    role_type: str = Field(10, description="角色类型")


class RoleDel(BaseModel):
    id: int = Field(..., description="角色id")