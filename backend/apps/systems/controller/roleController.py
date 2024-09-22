# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :roleController.py
# @Time      :2024/9/22 15:57
# @Author    :XiaoQi

from fastapi import APIRouter

from apps.systems.service.roleService import RolesService
from common.response.http_response import parter_success
from apps.systems.model.roleModel import RoleQuery, RoleIn, RoleDel

router = APIRouter()


@router.post('/list', description="获取角色列表")
async def all_roles(params: RoleQuery):
    data = await RolesService.list(params)
    return parter_success(data)


@router.post('/saveOrUpdate', description="新增或更新角色")
async def save_or_update(params: RoleIn):
    data = await RolesService.save_or_update(params)
    return parter_success(data)


@router.post('/deleted', description="删除角色")
async def deleted(params: RoleDel):
    data = await RolesService.deleted(params)
    return parter_success(data)
