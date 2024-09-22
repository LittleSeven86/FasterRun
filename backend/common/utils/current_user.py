# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from db.redis import redis_pool
from common.exception.BaseException import AccessTokenFail
from config.Config import config
from common.utils.local import g


async def current_user(token: str = None) -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
    """根据token获取用户信息"""

    user_info = await redis_pool.redis.get(config.TEST_USER_INFO.format(g.request.headers["token"] if not token else token))
    if not user_info:
        raise AccessTokenFail()
    return user_info
