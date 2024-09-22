# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :user_controller.py
# @Time      :2024/9/15 14:39
# @Author    :XiaoQi
from http.client import HTTPException

from fastapi import APIRouter
from sqlalchemy.dialects.postgresql.psycopg import logger
from starlette.requests import Request

from apps.systems.model.RoleModel import UserIn
from common.enum.code_enum import CodeEnum
from common.response.http_response import parter_success
from apps.systems.model.UserModel import User, UserLogin, UserQuery, UserResetPwd
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

@router.post("/logout",description="退出登录")
async def user_logout():
    await UsersService.user_logout()
    return parter_success()

@router.post("/get_userInfo",description="获取用户信息")
async def user_get_user_info(request:Request):
    """
    根据token，获取用户信息
    :param request:
    :return:
    """
    token = request.headers.get("token", None)
    if not token:
        raise CodeEnum.FAILURE_CODE_401("鉴权失败")
    user_info = await UsersService.get_userInfo_by_token(token)
    return parter_success(user_info)

@router.post("/list",description="用户列表")
async def user_list(request: UserQuery):
    data = await UsersService.list(request)
    return parter_success(data)

@router.post("/saveOrUpdate",description="更新保存用户")
async def user_save(request: UserIn):
    await UsersService.save_or_update(request)
    return parter_success()

@router.post("/resetPassword",description="重置密码")
async def user_reset_password(request: UserResetPwd):
    await UsersService.reset_password(request)
    return parter_success()


@router.get("/demo")
async def demo():
    return "success"