# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :sourceModel.py
# @Time      :2024/9/24 21:54
# @Author    :XiaoQi
import typing

from pydantic import Field
from common.model.BaseModel import BaseSchema


class SourceQuery(BaseSchema):
    id: int = Field(None, description="id")
    source_type: str = Field("mysql", description="数据源类型")
    name: str = Field(None, description="")
    source_ids: typing.List[int] = Field(None, description="")


class SourceIn(BaseSchema):
    id: int = Field(None, description="id")
    type: str = Field(None, description="数据源类型 mysql, redis, 等")
    name: str = Field(..., description="数据源名称")
    host: str = Field(None, description="地址")
    port: str = Field(None, description="端口")
    user: str = Field(None, description="用户名")
    password: str = Field(None, description="密码")


class EnvListSchema(BaseSchema):
    """环境序列化"""
    name: typing.Text
    url: str = Field(None, description="url")
    remarks: str = Field(None, description="备注")


class SourceId(BaseSchema):
    """环境序列化"""
    id: int = Field(..., description="id")


class EnvIn(BaseSchema):
    id: int = Field(None, description="")
    name: str = Field(None, description="环境名称")
    domain_name: str = Field(None, description="域名")
    remarks: str = Field(None, description="备注")
    headers: typing.List[typing.Dict[str, typing.Any]] = Field(None, description="请求头")
    variables: typing.List[typing.Dict[str, typing.Any]] = Field(None, description="变量")
    data_sources: typing.List[int] = Field(None, description="数据源 弃用")

class SourceInfo(BaseSchema):
    host: str
    port: int
    user: str
    password: str
    database: str = None


class ExecuteParam(BaseSchema):
    source_id: int
    database: str = ""
    sql: str


class SourceListQuery(BaseSchema):
    id: typing.Optional[typing.Union[str, None]]
    source_type: str = "mysql"
    env_id: typing.Optional[int]
    name: typing.Optional[str]


class SourceSaveSchema(BaseSchema):
    id: int = None
    type: str
    name: str
    host: str
    port: str
    user: str
    password: str
    env_id: int


class SourceIdIn(BaseSchema):
    source_id: int = Field(None, description="数据源id")


class SourceTableIn(BaseSchema):
    source_id: int = Field(None, description="数据源id")
    databases: str = Field(None, description="databases")


class CreateTableIn(BaseSchema):
    source_id: int = Field(None, description="数据源id")
    databases: str = Field(None, description="databases")
    table_name: str = Field(None, description="table_name")