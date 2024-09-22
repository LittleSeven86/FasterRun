# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :UsersService.py
# @Time      :2024/9/13 21:19
# @Author    :XiaoQi
import traceback
import typing
import uuid
from datetime import datetime
from urllib import request

import bcrypt
from fastapi import HTTPException
from loguru import logger
from starlette.status import HTTP_401_UNAUTHORIZED

from apps.systems.model.UserModel import UserTokenIn, UserLoginRecordIn, UserLogin
from common.enum.code_enum import CodeEnum
from apps.systems.dao.userDao import User, UserLoginRecord
from apps.systems.model.RoleModel import UserIn
from common.serialize.serialize import default_serialize
from common.utils.generate_rsa_key import decrypt_rsa_password
from common.utils.local import g
from config.Config import config
from db.redis import redis_pool

class UsersService:

    @staticmethod
    async def register(params: UserIn) -> User:
        """
        用户注册
        :param params:
        :return:
        """
        Isregister = await User.get_user_by_name(params.username)
        logger.info(Isregister)
        if Isregister:
            return ValueError(CodeEnum.USERNAME_OR_EMAIL_IS_REGISTER.msg)
        user = await  User.create(params.dict())
        return user

    async def login(params: UserLogin) -> UserTokenIn:
        """
        登录
        :return:
        """
        username = params.username
        password = params.password
        if not username and not password:
            raise ValueError(CodeEnum.PARTNER_CODE_PARAMS_FAIL.msg)
        user_info = await User.get_user_by_name(username)
        if not user_info:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        u_password = decrypt_rsa_password(user_info["password"])
        if u_password != password:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        token = str(uuid.uuid4())
        login_time = default_serialize(datetime.now())
        token_user_info = UserTokenIn(
            id=user_info["id"],
            token=token,
            avatar=user_info["avatar"],
            username=user_info["username"],
            nickname=user_info["nickname"],
            roles=user_info.get("roles", []),
            tags=user_info.get("tags", []),
            login_time=login_time,
            remarks=user_info["remarks"]
        )
        await redis_pool.redis.set(config.TEST_USER_INFO.format(token), token_user_info.dict(), config.CACHE_DAY)
        logger.info('用户 [{}] 登录了系统'.format(user_info["username"]))

        try:
            login_ip = g.request.headers.get("X-Real-IP", None)
            logger.info(login_ip)
            if not login_ip:
                login_ip = g.request.client.host
            params = UserLoginRecordIn(
                token=token,
                code=user_info["username"],
                user_id=user_info["id"],
                user_name=user_info["nickname"],
                login_type="password",
                login_time=login_time,
                login_ip=login_ip,
            )
            logger.info(params)
            await UsersService.user_login_record(params)
        except Exception as err:
            logger.error(f"登录日志记录错误\n{err}")
        return token_user_info

    @staticmethod
    async def get_user_info_by_token(token: str) -> UserTokenIn:
        """根据token获取用户信息"""
        token_user_info = await redis_pool.redis.get(config.TEST_USER_INFO.format(token))
        if not token_user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        user_info = await User.get(token_user_info.get("id"))
        if not user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        return UserTokenIn(
            id=user_info.id,
            token=token,
            avatar=user_info.avatar,
            username=user_info.username,
            nickname=user_info.nickname,
            roles=user_info.roles,
            tags=user_info.tags,
            login_time=token_user_info.get("login_time"),
            remarks=user_info.remarks
        )

    @staticmethod
    async def user_login_record(params: UserLoginRecordIn):
        result = await UserLoginRecord.create_or_update(params.dict())
        return result

    @staticmethod
    async def user_logout():
        """
        退登
        :return:
        """
        token = g.request.headers.get("token", None)
        try:
            await redis_pool.redis.delete(config.TEST_USER_INFO.format(token))
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    async def get_userInfo_by_token(token: str) -> UserTokenIn:
        """
        根据token获取用户信息
        :param token:
        :return:
        """
        token_info = await redis_pool.redis.get(config.TEST_USER_INFO.format(token))
        if not token_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        user_info = await User.get(token_info.get("id"))
        if not user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        return UserTokenIn(
            id=user_info.id,
            token=token,
            avatar=user_info.avatar,
            username=user_info.username,
            nickname=user_info.nickname,
            roles=user_info.roles,
            tags=user_info.tags,
            remarks=user_info.remarks,
            login_time=token_info.get("login_time"),
        )