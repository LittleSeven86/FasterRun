# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :moduleDao.py
# @Time      :2024/9/22 22:24
# @Author    :XiaoQi
import typing

from sqlalchemy import String, BigInteger, Integer, select, func, distinct, and_, text
from sqlalchemy.orm import mapped_column, aliased


from apps.systems.dao.userDao import User
from common.dao.base import Base
from apps.module.model.moduleModel import ModuleQuery
from apps.project.dao.projectDao import ProjectDao



class ModuleDao(Base):
    """模块表"""
    __tablename__ = 'module_info'

    name = mapped_column(String(64), nullable=False, comment='模块名称', index=True)
    project_id = mapped_column(BigInteger, comment='归属项目id')
    config_id = mapped_column(Integer, comment='关联配置id')
    test_user = mapped_column(String(100), comment='测试负责人')
    simple_desc = mapped_column(String(100), comment='简要描述')
    remarks = mapped_column(String(100), comment='其他信息')
    module_packages = mapped_column(String(64), comment='模块对应的包名称')
    leader_user = mapped_column(String(100), comment='负责人')
    priority = mapped_column(Integer, comment='默认执行用例优先级', default=4)

    # packages_id = mapped_column(Integer,  comment='包id')

    @classmethod
    async def get_list(cls, params: ModuleQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.project_name:
            q.append(ProjectDao.name.like('%{}%'.format(params.project_name)))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        # if packages_id:
        #     q.append(cls.packages_id == packages_id)
        if params.sort_type == 0:
            sort_type = 'asc'
        else:
            sort_type = 'desc'
        if not params.order_field or params.order_field == 'creation_date':
            params.order_field = 'module_info.creation_date'
        if params.order_field == 'project_name':
            params.order_field = 'project_info.name'
        if params.order_field == 'test_user':
            params.order_field = 'user.nickname'
        order_by = '{} {} {} {}'.format(params.order_field, sort_type, ',module_info.id', sort_type)
        u = aliased(User)

        from apps.api_info.dao.apiInfoDao import ApiInfoDao
        stmt = select(cls.get_table_columns(),\
                      func.count(distinct(ApiInfoDao.id)).label('case_count'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'),
                      ProjectDao.name.label('project_name')).where(*q) \
            .outerjoin(ProjectDao, and_(cls.project_id == ProjectDao.id, ProjectDao.enabled_flag == 1)) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ApiInfoDao, and_(cls.id == ApiInfoDao.module_id, ApiInfoDao.enabled_flag == 1)) \
            .group_by(cls.id).order_by(text(order_by))
        return await cls.pagination(stmt)

    @classmethod
    async def get_module_by_project_id(cls, project_id: int):
        """查询项目是否有关联模块"""
        stmt = select(cls.id).where(cls.project_id == project_id, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_module_by_name(cls, name: str):
        stmt = select(cls.id).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    def get_module_by_id(cls, id):
        return cls.query.filter(cls.id == id, cls.enabled_flag == 1).first()

    @classmethod
    async def get_module_info_byId(cls,id):
        stmt = select(cls.get_table_columns()).where(cls.id == id)
        return await cls.get_result(stmt)

    @classmethod
    async def search_by_moduleName(cls, name: str):
        if not name:
            stmt = select(cls)
            return await cls.get_result(stmt)
        stmt = select(cls.get_table_columns())\
                .where(cls.name.ilike(f"%{name}%"), cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    def get_module_by_module_packages(cls, module_packages):
        return cls.query.filter(cls.module_packages == module_packages, cls.enabled_flag == 1).all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_module_by_packages_id(cls, packages_id):
        return cls.query.filter(cls.packages_id == packages_id, cls.enabled_flag == 1).first()




