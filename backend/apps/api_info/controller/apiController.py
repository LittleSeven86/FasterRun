# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :apiCaseController.py
# @Time      :2024/9/24 21:23
# @Author    :XiaoQi
import json
from urllib import request

from fastapi import APIRouter

from apps.api_info.model.apiInfoModel import ApiQuery, ApiInfoIn, ApiIds, ApiId, ApiRunSchema
from apps.api_info.service.apiInfoService import ApiInfoService
from common.response.http_response import parter_success
from common.utils.current_user import current_user

router = APIRouter()

router = APIRouter()


@router.post('/list', description="获取接口列表")
async def api_list(params: ApiQuery):
    result = await ApiInfoService.list(params)
    return parter_success(result)


@router.post('/getApiInfo', description="获接口信息详情")
async def get_case_info(params: ApiId):
    """
    获取用例信息
    :return:
    """
    case_info = await ApiInfoService.detail(params)
    return parter_success(case_info)


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


@router.post('/runApi', description="运行接口")
async def run_api(params: ApiRunSchema):
    """
    运行api
    :return:
    """
    current_user_info = await current_user()
    params.exec_user_id = current_user_info.get("id", None)
    params.exec_user_name = current_user_info.get("nickname", None)
    summary = await ApiInfoService.run_api(params)
    if params.run_mode == 20:
        return parter_success(code=0, msg='用例执行中，请稍后查看报告即可,默认模块名称命名报告')
    else:
        return parter_success(summary)


@router.post('/debugApi', description="debug接口")
async def debug_api(params: ApiInfoIn):
    data = await ApiInfoService.debug_api(params)
    return parter_success(data)


@router.post('/postman2case', description="文件转用例")
def postman2case():
    """
    postman 文件转用例
    :return:
    """
    postman_file = request.files.get('file', None)
    if not postman_file:
        return parter_success(code=codes.PARTNER_CODE_FAIL, msg='请选择导入的postman，json文件！')
    if postman_file.filename.split('.')[-1] != 'json':
        return parter_success(code=codes.PARTNER_CODE_FAIL, msg='请选择json文件导入！')
    json_body = json.load(postman_file)
    data = ApiInfoService.postman2api(json_body, **request.form)
    return parter_success(data)


@router.post('/getUseApiRelation', description="api使用关系")
async def use_api_relation(params: ApiId):
    """
    测试报告
    :return:
    """
    data = await ApiInfoService.use_api_relation(params)
    return parter_success(data)

