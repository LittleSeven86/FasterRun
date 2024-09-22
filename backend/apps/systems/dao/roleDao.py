# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :roleDao.py
# @Time      :2024/9/22 15:57
# @Author    :XiaoQi
import typing

from sqlalchemy import String, Integer, select
from sqlalchemy.orm import mapped_column, aliased

from apps.systems.dao.userDao import User
from apps.systems.model.roleModel import RoleQuery
from common.dao.base import Base

class Roles(Base):
    """角色表"""
    __tablename__ = 'roles'

    name = mapped_column(String(64), nullable=False, comment='菜单名称', index=True)
    role_type = mapped_column(Integer, comment='权限类型，10菜单权限，20用户组权限', index=True, default=10)
    menus = mapped_column(String(64), comment='菜单列表', index=True)
    description = mapped_column(Integer, comment='描述')
    status = mapped_column(Integer, comment='状态 10 启用 20 禁用', default=10)

    @classmethod
    async def get_list(cls, params: RoleQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.role_type:
            q.append(cls.role_type == params.role_type)
        else:
            q.append(cls.role_type == 10)
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label("created_by_name"),
                      User.nickname.label("updated_by_name")) \
            .where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .outerjoin(User, User.id == cls.updated_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_roles_by_ids(cls, ids: typing.List, role_type=None):
        q = [cls.enabled_flag == 1, cls.id.in_(ids)]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)

        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    def get_all(cls, role_type=10):
        q = list()
        if role_type:
            q.append(cls.role_type == role_type)
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.id.desc())

    @classmethod
    async def get_roles_by_name(cls, name, role_type=None):
        q = [cls.name == name, cls.enabled_flag == 1]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt, True)