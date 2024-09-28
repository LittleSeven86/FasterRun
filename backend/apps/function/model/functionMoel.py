# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :functionMoel.py
# @Time      :2024/9/28 21:17
# @Author    :XiaoQi

import typing

from pydantic import BaseModel, Field
from common.model.BaseModel import BaseSchema


class FuncQuery(BaseSchema):
    """查询参数序列化"""

    id: int = Field(None, description="id")
    ids: typing.List[int] = Field(None, description="ids")
    project_name: str = Field(None, description="项目名称")
    name: str = Field(None, description="脚本名称")
    common: str = Field(None, description="")


class FuncListQuery(BaseSchema):
    """查询参数序列化"""

    id: int = Field(None, description="id")
    func_name: str = Field(None, description="函数名")


class FuncListSchema(BaseSchema):
    """自定义函数"""
    project_id: typing.Optional[int]
    name: str = Field(None, description="")
    content: str = Field(None, description="")


class FuncIn(BaseModel):
    id: int = Field(None, description="id")
    content: str = Field(None, description="")
    project_id: str = Field(None, description="")
    name: str = Field(None, description="")
    remarks: str = Field(None, description="")


class FuncDebug(BaseModel):
    id: int = Field(None, description="id")
    func_parse_str: str = Field(None, description="")
    func_name: str = Field(None, description="")
    args_info: typing.Dict[typing.Text, typing.Any] = Field({}, description="")


class FuncId(BaseModel):
    id: int = Field(..., description="id")

