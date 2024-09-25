# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :envDao.py
# @Time      :2024/9/25 20:25
# @Author    :XiaoQi
from loguru import logger
from sqlalchemy import String, JSON, select, Integer, update
from sqlalchemy.orm import mapped_column, aliased

from apps.env.dao.dataSourceDao import DataSourceDao
from apps.env.model.envModel import EnvQuery, BindingDataSourceIn, BindingFuncIn
from apps.systems.dao.userDao import User
from common.dao.base import Base


class Env(Base):
    """环境表"""
    __tablename__ = 'env'

    name = mapped_column(String(255), nullable=False, comment='环境名称', index=True)
    domain_name = mapped_column(String(255), comment='url地址')
    remarks = mapped_column(String(255), comment='说明')
    variables = mapped_column(JSON(), comment='环境变量')
    headers = mapped_column(JSON(), comment='环境请求头')
    data_sources = mapped_column(JSON(), comment='数据源')

    @classmethod
    async def get_list(cls, params: EnvQuery = EnvQuery()):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        u = aliased(User)
        stmt = select(cls.id,
                      cls.name,
                      cls.domain_name,
                      cls.variables,
                      cls.headers,
                      cls.remarks,
                      cls.updated_by,
                      cls.created_by,
                      cls.creation_date,
                      cls.updation_date,
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'), ).where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取环境"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)


class EnvDataSource(Base):
    """环境数据源关联表"""
    __tablename__ = 'env_data_source'

    env_id = mapped_column(Integer, nullable=False, index=True, comment='环境id')
    data_source_id = mapped_column(Integer, nullable=False, index=True, comment='数据源id')

    @classmethod
    async def unbinding_data_source(cls, params: BindingDataSourceIn):
        stmt = update(cls).where(cls.enabled_flag == 1,
                                 cls.env_id == params.env_id,
                                 cls.data_source_id.in_(params.data_source_ids)) \
            .values(enabled_flag=0)
        return await cls.execute(stmt)

    @classmethod
    async def get_by_env_id(cls, env_id: int):
        q = [cls.enabled_flag == 1, cls.env_id == env_id]
        stmt = select(cls.id,
                      cls.env_id.label("env_id"),
                      Env.name.label("env_name"),
                      DataSourceDao.name,
                      DataSourceDao.id.label("data_source_id"),
                      DataSourceDao.host,
                      DataSourceDao.port,
                      DataSourceDao.type,
                      DataSourceDao.user,
                      DataSourceDao.updation_date,
                      DataSourceDao.creation_date,
                      ) \
            .where(*q) \
            .outerjoin(Env, Env.id == cls.env_id) \
            .outerjoin(DataSourceDao, DataSourceDao.id == cls.data_source_id) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取数据"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        await cls.get_result(stmt, first=True)


class EnvFunc(Base):
    """环境数据源管理表"""
    __tablename__ = 'env_func'

    env_id = mapped_column(Integer, nullable=False, index=True, comment='环境id')
    func_id = mapped_column(Integer, nullable=False, index=True, comment='辅助函数id')

    @classmethod
    async def unbinding_funcs(cls, params: BindingFuncIn):
        stmt = update(cls).where(cls.enabled_flag == 1,
                                 cls.env_id == params.env_id,
                                 cls.func_id.in_(params.func_ids)) \
            .values(enabled_flag=0)
        return await cls.execute(stmt)

    @classmethod
    async def get_by_env_id(cls, env_id: int, Functions=None):
        q = [cls.enabled_flag == 1, cls.env_id == env_id]
        stmt = select(cls.get_table_columns(),
                      cls.env_id.label("env_id"),
                      Env.name.label("env_name"),
                      Functions.name.label("name"),
                      Functions.remarks.label("remarks"),
                      Functions.content.label("content"),
                      Functions.id.label("func_id"),
                      ) \
            .where(*q) \
            .outerjoin(Env, Env.id == cls.env_id) \
            .outerjoin(Functions, Functions.id == cls.func_id) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_env_by_name(cls, name):
        """根据环境名称获取数据"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        await cls.get_result(stmt, first=True)