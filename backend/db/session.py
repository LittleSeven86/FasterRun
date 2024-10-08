# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :session.py
# @Time      :2024/9/13 21:56
# @Author    :XiaoQi
import functools
import traceback
import typing
from asyncio import current_task
from contextvars import ContextVar

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import sessionmaker

from common.utils.local import g
from config.Config import config

SQLAlchemySession: ContextVar[typing.Optional[AsyncSession]] = ContextVar('SQLAlchemySession', default=None)

# 创建表引擎
async_engine = create_async_engine(
    url=config.DATABASE_URI,
    echo=config.DATABASE_ECHO,
    pool_size=config.DATABASE_POOL_SIZE,
    max_overflow=config.MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=config.POOL_RECYCLE,
)

# 操作表会话
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

async_session = async_scoped_session(async_session_factory, scopefunc=current_task)

sync_engine = create_engine(
    url=config.DATABASE_URI,
    echo=config.DATABASE_ECHO,
    pool_size=config.DATABASE_POOL_SIZE,
    max_overflow=config.MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=config.POOL_RECYCLE,
)
sync_engine_facttory = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
sync_session = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False, expire_on_commit=False)

def provide_async_session(func):
    """
    装饰器: 自动处理数据库会话的创建、提交和回滚。
    如果函数已经接收了一个 `session` 参数，则使用它；否则，创建新的会话。
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        session_provided = False
        func_params = func.__code__.co_varnames[:func.__code__.co_argcount]

        if 'session' in func_params:
            index = func_params.index('session')
            if index < len(args) or 'session' in kwargs:
                session_provided = True

        if session_provided:
            return await func(*args, **kwargs)

        async with async_session() as session:
            try:
                result = await func(*args, session=session, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                logger.error(traceback.format_exc())
                await session.rollback()
                raise

    return wrapper

def provide_async_session_router(func: typing.Callable):
    """
    装饰器：为路由提供全局错误回滚。
    :param func: 函数
    :return: 被装饰的函数
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            g.zero_db_session = session
            try:
                return await func(*args, **kwargs)
            except (IntegrityError, Exception) as e:
                await session.rollback()
                logger.error(f"An error occurred: {e}", exc_info=True)
                raise
            finally:
                await session.commit()
    return wrapper
