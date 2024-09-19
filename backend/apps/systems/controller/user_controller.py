# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :user_controller.py
# @Time      :2024/9/15 14:39
# @Author    :XiaoQi

from fastapi import APIRouter

from common.response.http_response import parter_success
from apps.systems.model.UserModel import User
from apps.systems.service.UsersService import UsersService

router = APIRouter()


@router.post("/userRegister",description="用户注册")
async def user_register(request: User):
    data = await UsersService.register(request)
    return parter_success(data)