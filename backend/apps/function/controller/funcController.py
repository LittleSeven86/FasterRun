# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :funcController.py
# @Time      :2024/9/28 21:42
# @Author    :XiaoQi

from fastapi import APIRouter

from common.response.http_response import parter_success
from apps.function.model.functionMoel import FuncQuery, FuncListQuery, FuncIn, FuncDebug, FuncId
from apps.function.service.functionService import FunctionsService

router = APIRouter()


@router.post('/list', description="获取自定义函数列表")
async def get_debug_talk_list(params: FuncQuery):
    data = await FunctionsService.list(params)
    return parter_success(data)


@router.post('/getFuncInfo', description="获取自定义函数详情")
async def get_debug_talk_info(params: FuncQuery):
    data = await FunctionsService.get_function_info(params)
    return parter_success(data)


@router.post('/saveOrUpdate', description="更新保存")
async def save_debug_talk(params: FuncIn):
    """
    更新保存
    :return:
    """
    # return parter_success(code=codes.PARTNER_CODE_FAIL, msg='演示环境不保存！')
    data = await FunctionsService.save_or_update(params)
    return parter_success(data)


@router.post('/getFuncList', description="获取函数列表")
async def get_func_list(params: FuncListQuery):
    try:
        data = await FunctionsService.get_function_by_id(params)
        func_list = data.get('func_list')
        return parter_success(func_list)
    except Exception as err:
        raise ValueError(f"查询函数名称失败:{err}")


@router.post('/debugFunc', description="脚本调试")
async def debug_func(params: FuncDebug):
    result = await FunctionsService.debug_func(params)
    return parter_success({'result': result})


@router.post('/deleted', description="删除脚本")
async def debug_func(params: FuncId):
    data = await FunctionsService.deleted(params)
    return parter_success(data)
