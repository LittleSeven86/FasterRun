# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :menuController.py
# @Time      :2024/9/22 14:54
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.systems.model.menuModel import MenuViews, MenuIn, MenuDel
from apps.systems.service.menuService import MenuService
from common.response.http_response import parter_success

router = APIRouter()

@router.get('/allMenu',description="获取所有菜单数据")
async def allMenu():
    data = await MenuService.all_menus()
    return parter_success(data)


@router.post('/getAllMenus', description="获取菜单嵌套结构")
async def get_all_menus():
    data = await MenuService.all_menu_nesting()
    return parter_success(data)

@router.post('/saveOrUpdate', description="新增或者更新menu")
async def save_or_update(params: MenuIn):
    # return partner_success(code=codes.PARTNER_CODE_FAIL, msg="演示环境不保存！")
    await MenuService.save_or_update(params)
    return parter_success()


@router.post('/deleted', description="删除菜单")
async def delete_menu(params: MenuDel):
    data = await MenuService.deleted(params)
    return parter_success(data)

@router.post('/setMenuViews', description="设置菜单访问量")
async def set_menu_views(params: MenuViews):
    data = await MenuService.set_menu_views(params)
    return parter_success(data)

