# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :moduleController.py
# @Time      :2024/9/22 22:24
# @Author    :XiaoQi

from fastapi import APIRouter

from apps.module.dao.moduleDao import ModuleDao
from apps.module.model.moduleModel import ModuleQuery, ModuleIn, ModuleId
from apps.module.service.moduleService import ModuleService
from common.response.http_response import parter_success

router = APIRouter()



@router.post('/list', description="模块列表")
async def module_list(params: ModuleQuery):
    data = await ModuleService.list(params)
    return parter_success(data)

@router.get("/info/{module_id}")
async def module_info(module_id: int):
    data = await ModuleService.get_byId(module_id)
    return parter_success(data)

@router.get("/search/",description="通过模块名模糊搜索")
async def module_search(module_name: str = None):
    data = await ModuleService.search_byName(module_name)
    return parter_success(data)

@router.get('/getAllModule', description="获取所有模块")
async def get_all_module():
    data = await ModuleService.get_all()
    return parter_success(data)


@router.put('/saveOrUpdate', description="更新保存项目")
async def save_or_update(params: ModuleIn):
    data = await ModuleService.save_or_update(params)
    return parter_success(data)


@router.post('/deleted', description="删除模块")
async def deleted(params: ModuleId):
    data = await ModuleService.deleted(params)
    return parter_success(data)