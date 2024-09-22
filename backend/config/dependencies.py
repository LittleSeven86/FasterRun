# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :dependencies.py
# @Time      :2024/9/21 17:30
# @Author    :XiaoQi
from fastapi import Request, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.dialects.postgresql.psycopg import logger

from db.redis import redis_pool
from common.exception.BaseException import AccessTokenFail
from common.utils.local import g
from config.Config import config


class MyAPIKeyHeader(APIKeyHeader):
    """"""

    def __init__(self):
        super().__init__(name="token", auto_error=False)

    async def __call__(self, request: Request):
        g.request = request
        path: str = request.get('path')
        if path in config.WHITE_ROUTER:
            return
        token: str = request.headers.get("token")
        if not token:
            raise AccessTokenFail()
        user_info = await redis_pool.redis.get(config.TEST_USER_INFO.format(token))
        if not user_info:
            raise AccessTokenFail()
        # 重置token时间
        await redis_pool.redis.set(config.TEST_USER_INFO.format(token), user_info, config.CACHE_DAY)
        return


async def login_verification(token: Security = Security(MyAPIKeyHeader())):
    """
    登录校验
    :param token: token
    :return:
    """
    pass