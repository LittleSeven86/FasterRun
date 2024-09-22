# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :projectDao.py
# @Time      :2024/9/12 21:34
# @Author    :XiaoQi

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import aliased, mapped_column
from watchfiles import awatch

from apps.systems.dao.userDao import User
from apps.project.model.projectModel import ProjectQuery
from common.dao.base import Base


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
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.id:
            q.append(cls.id == params.id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        # 使用 aliased 优化表连接
        u = aliased(User)

        # 构建查询语句
        stmt = select(
            cls.get_table_columns(),
            u.nickname.label('updated_by_name'),
            User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        # 执行带分页的查询
        return await cls.pagination(stmt)

    @classmethod
    async def get_project_byId(cls, id: int):
        """
        使用项目id查询项目基本信息
        :param id:
        :return:
        """
        dto = select(cls.get_table_columns()) \
            .where(cls.id == id, cls.enabled_flag == 1)
        return await cls.get_result(dto)

    @classmethod
    async def get_project_id_tolist(cls):
        """
        查询enabled_flag==1， 并返回指定字段
        :return:
        """
        dto = cls.query.filter(cls.enabled_flag == 1)\
                .with_entities(cls.id,
                               cls.responsible_name,
                               cls.test_user,
                               cls.dev_user,
                               cls.created_by)\
                .all
        return dto

    @classmethod
    async def get_project_by_name(cls, name: str):
        dto = select(cls.id).where(cls.name == name,cls.enabled_flag == 1)
        return await cls.get_result(dto,first=True)

    @classmethod
    def get_count(cls):
        dto = cls.query.filter(cls.enabled_flag == 1).count()
        return dto

    @classmethod
    def get_project_ids(cls):
        return cls.query.filter(cls.enabled_flag == 1).with_entities(cls.id).all()

    @classmethod
    def get_project_by_product_id(cls, product_id):
        return cls.query.filter(cls.enabled_flag == 1, cls.product_id == product_id).with_entities(cls.id).all()


