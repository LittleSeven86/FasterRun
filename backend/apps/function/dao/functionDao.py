# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :functionDao.py
# @Time      :2024/9/28 21:20
# @Author    :XiaoQi

from sqlalchemy import Integer, Text, String, select
from sqlalchemy.orm import mapped_column, aliased

from apps.function.model.functionMoel import FuncQuery
from apps.project.dao.projectDao import ProjectDao
from apps.systems.dao.userDao import User
from common.dao.base import Base


class Functions(Base):
    __tablename__ = 'functions'

    name = mapped_column(Integer, nullable=False, comment='name')
    remarks = mapped_column(Integer, comment='备注')
    project_id = mapped_column(Integer, comment='关联项目')
    content = mapped_column(Text, comment='自定义函数内容')
    func_type = mapped_column(String(255), comment='函数类型')
    func_tags = mapped_column(String(255), comment='函数标签')

    @classmethod
    async def get_list(cls, params: FuncQuery):
        q = [cls.enabled_flag == 1]
        if params.project_name:
            q.append(ProjectDao.name.like(f'%{params.project_name}%'))
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        u = aliased(User)

        stmt = select(cls.get_table_columns(),
                      ProjectDao.name.label('project_name'),
                      User.nickname.label('updated_by_name'),
                      u.nickname.label('created_by_name'), ).where(*q) \
            .outerjoin(ProjectDao, cls.project_id == ProjectDao.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .outerjoin(u, u.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_by_id(cls, id: int):
        stmt = select(cls.get_table_columns(),
                      ProjectDao.name.label('project_name')).where(cls.enabled_flag == 1, cls.id == id) \
            .outerjoin(ProjectDao, cls.project_id == ProjectDao.id)

        return await cls.get_result(stmt, first=True)

    @classmethod
    def get_by_project_id(cls, project_id):
        return cls.query.filter(cls.project_id == project_id).first()

    @classmethod
    async def all_func(cls):
        dto = select()