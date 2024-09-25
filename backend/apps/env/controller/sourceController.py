# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :sourceController.py
# @Time      :2024/9/24 22:07
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.env.model.sourceModel import SourceQuery, SourceIn, SourceId, SourceInfo, SourceIdIn, SourceTableIn, \
    ExecuteParam, CreateTableIn
from apps.env.service.dataSource import DsService
from common.response.http_response import parter_success

router = APIRouter()

@router.get("/all",description="查询全部")
async def get_all():
    data = await DsService.get_allSource()
    return parter_success(data)


@router.post('/sourceList', description="获取数据源列表")
async def get_source_list(params: SourceQuery):
    data = await DsService.get_source_list(params)
    return parter_success(data)


@router.post('/source', description="保存")
async def save_or_update_source(params: SourceIn):
    data = await DsService.save_or_update(params)
    return parter_success(data)


@router.post('/deletedSource', description="删除")
async def deleted_source(params: SourceId):
    data = await DsService.deleted_source(params)
    return parter_success(data)


@router.post('/testConnect', description="测试连接")
async def test_connect(params: SourceInfo):
    """
    测试连接
    :return:
    """
    data = await DsService.test_connect(params)
    return parter_success(data)


@router.post('/dbList', description="数据列表")
async def get_source_list(params: SourceIdIn):
    data = await DsService.get_db_list(params)
    return parter_success(data)


@router.post('/tableList', description="表列表")
async def get_table_list(params: SourceTableIn):
    """
    表列表
    :return:
    """
    data = await DsService.get_table_list(params)
    return parter_success(data)


@router.post('/columnList', description="获取表字段")
async def get_column_list(params: SourceTableIn):
    data = await DsService.get_column_list(params.source_id, params.databases)
    return parter_success(data)


@router.post('/mysql/execute', description="mysql 查询")
async def mysql_execute(params: ExecuteParam):
    data = await DsService.execute(params)
    return parter_success(data)


@router.post('/showCreateTable', description="查询建表语句")
async def show_create_table(params: CreateTableIn):
    data = await DsService.show_create_table(params)
    return parter_success(data)