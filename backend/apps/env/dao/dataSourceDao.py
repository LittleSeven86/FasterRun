# coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :dataSourceDao.py
# @Time      :2024/9/24 21:56
# @Author    :XiaoQi
import typing

from loguru import logger
from sqlalchemy import String, select
from sqlalchemy.orm import mapped_column, aliased

from apps.env.model.sourceModel import SourceQuery
from apps.systems.dao.userDao import User
from common.dao.base import Base

class DataSourceDao(Base):
    """数据源"""
    __tablename__ = 'data_source'

    type = mapped_column(String(255), comment='数据源类型', index=True)
    name = mapped_column(String(255), nullable=False, comment='数据源名称', index=True)
    host = mapped_column(String(255), comment='ip')
    port = mapped_column(String(255), comment='端口')
    user = mapped_column(String(255), comment='用户名')
    password = mapped_column(String(255), comment='密码')

    @classmethod
    async def get_list(cls, params: SourceQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.source_type:
            q.append(cls.type == params.source_type)
        if params.name:
            q.append(cls.name.like(f"%{params.name}%"))
        if params.source_ids and isinstance(params.source_ids, list):
            q.append(cls.id.in_(params.source_ids))
        u = aliased(User)
        stmt = select(cls.get_table_columns(exclude={"password"}),
                      u.nickname.label('created_by_name'),
                      User.nickname.label('updated_by_name'),
                      ).where(*q) \
            .outerjoin(User, cls.updated_by == User.id) \
            .outerjoin(u, cls.created_by == u.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    def get_user_by_name(cls, username):
        return cls.query.filter(cls.username == username, cls.enabled_flag == 1).first()

    @classmethod
    def get_allSource(cls):
        return cls.get_result(select(cls))
