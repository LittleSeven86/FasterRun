# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :user_controller.py
# @Time      :2024/9/15 14:39
# @Author    :XiaoQi

from fastapi import APIRouter
from sqlalchemy.dialects.postgresql.psycopg import logger

from common.response.http_response import parter_success
from apps.systems.model.UserModel import User, UserLogin
from apps.systems.service.UsersService import UsersService
from common.utils.local import g

router = APIRouter()


@router.post("/register",description="用户注册")
async def user_register(request: User):
    data = await UsersService.register(request)
    return parter_success(data)

@router.post("/login",description="登录")
async def user_login(request: UserLogin):
    data = await UsersService.login(request)
    logger.info(data)
    return parter_success(data,msg="登录成功")

@router.get("/demo")
async def demo():
    return "success"