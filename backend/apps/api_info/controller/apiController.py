# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :apiCaseController.py
# @Time      :2024/9/24 21:23
# @Author    :XiaoQi

from fastapi import APIRouter

from apps.api_info.model.apiInfoModel import ApiQuery, ApiInfoIn, ApiIds, ApiId
from apps.api_info.service.apiInfoService import ApiInfoService
from common.response.http_response import parter_success

router = APIRouter()

@router.get("/info",description="获取接口信息详情")
async def info(id:int):
    """
    根据id获取接口的信息
    :param id: 
    :return: 
    """
    info = await ApiInfoService.detail(id)
    return parter_success(info)

@router.post('/list', description="获取接口列表")
async def api_list(params: ApiQuery):
    result = await ApiInfoService.list(params)
    return parter_success(result)


@router.post('/getApiInfos', description="获接口信息详情多个")
async def get_case_infos(params: ApiIds):
    """
    获取用例信息
    :return:
    """
    case_info = await ApiInfoService.get_detail_by_ids(params)
    return parter_success(case_info)


@router.post('/saveOrUpdate', description="更新保存接口")
async def save_or_update(params: ApiInfoIn):
    case_info = await ApiInfoService.save_or_update(params)
    return parter_success(case_info)


@router.post('/copyApi', description="复制接口")
async def copy_api(params: ApiId):
    await ApiInfoService.copy_api(params)
    return parter_success()


@router.post('/setApiStatus', description="接口失效生效")
async def set_api_status():
    await ApiInfoService.set_api_status(**parsed_data)
    return parter_success()


@router.post('/deleted', description="删除接口")
async def deleted(params: ApiId):
    """
    删除用例
    :return:
    """
    data = await ApiInfoService.deleted(params.id)
    return parter_success(data)
