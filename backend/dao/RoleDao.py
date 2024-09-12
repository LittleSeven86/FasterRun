# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :RoleDao.py
# @Time      :2024/9/12 21:47
# @Author    :XiaoQi
import typing

from sqlalchemy import String, Text, JSON, Integer, select
from sqlalchemy.orm import mapped_column, aliased

from dao.Base import Base
from entity import RoleModel


class User(Base):
    """用户表"""
    __tablename__ = 'user'

    username = mapped_column(String(64), nullable=False, comment='用户名', index=True)
    password = mapped_column(Text, nullable=False, comment='密码')
    email = mapped_column(String(64), comment='邮箱')
    roles = mapped_column(JSON, comment='用户类型')
    status = mapped_column(Integer, comment='用户状态  1 锁定， 0 正常', default=0)
    nickname = mapped_column(String(255), comment='用户昵称')
    user_type = mapped_column(Integer, comment='用户类型 10 管理人员, 20 测试人员', default=20)
    remarks = mapped_column(String(255), comment='用户描述')
    avatar = mapped_column(Text, comment='头像')
    tags = mapped_column(JSON, comment='标签')

    @classmethod
    async def get_list(cls, params: RoleModel):
        q = [cls.enabled_flag == 1]
        # todo 将添加条件的语法抽为一层公共方法
        if params.username:
            q.append(cls.username.like('%{}%'.format(params.username)))
        if params.nickname:
            q.append(cls.nickname.like('%{}%'.format(params.nickname)))
        if params.user_ids and isinstance(params.user_ids, list):
            q.append(cls.id.in_(params.user_ids))
        # *[getattr(cls, c.name) for c in cls.__table__.columns]
        u = aliased(User)
        stmt = select(*cls.get_table_columns(), u.nickname.label("created_by_name")) \
            .where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_user_by_roles(cls, roles_id: int) -> typing.Any:
        stmt = select(cls.id).where(cls.roles.like(f'%{roles_id}%'), cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_user_by_name(cls, username: str):
        stmt = select(*cls.get_table_columns()).where(cls.username == username, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_user_by_nickname(cls, nickname: str):
        stmt = select(*cls.get_table_columns()).where(cls.nickname == nickname, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)
