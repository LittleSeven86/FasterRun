# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ProjectDao.py
# @Time      :2024/9/12 21:34
# @Author    :XiaoQi

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import aliased, mapped_column
from apps.systems.dao.RoleDao import User
from apps.project.model.ProjectInfoModel import ProjectQuery


class ProjectDao(Base):
    """
    项目基本信息表
    """
    __tablename__ = 'project_info'

    name = mapped_column(String(64), nullable=False, index=True, comment="项目名称")
    responsible_name = mapped_column(String(64), comment='负责人')
    test_user = mapped_column(String(100), comment='测试人员')
    dev_user = mapped_column(String(100), comment='开发人员')
    publish_app = mapped_column(String(100), comment='发布应用')
    simple_desc = mapped_column(String(100), comment='简要描述')
    remarks = mapped_column(String(100), comment='其他信息')
    config_id = mapped_column(Integer, comment='关联配置id')
    product_id = mapped_column(Integer, comment='产品线id')

    @classmethod
    async def get_list(cls, params: ProjectQuery):
        q = [cls.enabled_flag == 1]

        # 添加查询条件的函数，避免重复代码
        def add_query_condition(condition, query):
            if condition:
                q.append(query)

        # 使用 f-string 替代 format，提升性能
        add_query_condition(params.name, cls.name.like(f'%{params.name}%'))
        add_query_condition(params.created_by_name, User.nickname.like(f'%{params.created_by_name}%'))
        add_query_condition(params.id, cls.id == params.id)
        add_query_condition(params.ids, cls.id.in_(params.ids))

        # 使用 aliased 优化表连接
        u = aliased(User)

        # 构建查询语句
        stmt = select(
            cls.get_table_columns(),
            u.nickname.label('updated_by_name'),
            User.nickname.label('created_by_name')
        ).where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())

        # 执行带分页的查询
        return await cls.pagination(stmt)

