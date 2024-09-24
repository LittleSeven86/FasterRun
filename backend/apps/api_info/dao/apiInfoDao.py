# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ApiInfoDaoDao.py
# @Time      :2024/9/23 21:29
# @Author    :XiaoQi
import typing

from sqlalchemy import String, BigInteger, Integer, JSON, Text, select, text, func, Boolean, and_, distinct
from sqlalchemy.orm import mapped_column, aliased

from apps.api_case.model.apiCaseModel import ApiCaseQuery
from apps.api_info.model.apiInfoModel import ApiQuery, ApiIds
from apps.module.dao.moduleDao import ModuleDao
from apps.project.dao.projectDao import ProjectDao
from apps.systems.dao.userDao import User
from common.dao.base import Base


class ApiInfoDao(Base):
    """接口用例"""
    __tablename__ = 'api_info'

    name = mapped_column(String(255), nullable=False, comment="用例名称", index=True)
    project_id = mapped_column(BigInteger, nullable=False, comment='所属项目')
    module_id = mapped_column(BigInteger, nullable=False, comment='所属模块')
    status = mapped_column(Integer, comment='用例状态 10, 生效 ， 20 失效', default=10)
    code_id = mapped_column(BigInteger, comment='关联接口id')
    code = mapped_column(String(255), comment='接口code')
    priority = mapped_column(Integer, comment='优先级', default=3)
    tags = mapped_column(JSON, comment='用例标签')
    url = mapped_column(String(255), nullable=False, comment='请求地址')
    method = mapped_column(String(255), comment='请求方式')
    remarks = mapped_column(String(255), comment='描述')
    step_type = mapped_column(String(255), comment='描述')
    pre_steps = mapped_column(JSON, comment='前置步骤')
    post_steps = mapped_column(JSON, comment='后置步骤')
    setup_code = mapped_column(Text, comment='前置code')
    teardown_code = mapped_column(Text, comment='后置code')
    setup_hooks = mapped_column(JSON, comment='前置操作')
    teardown_hooks = mapped_column(JSON, comment='后置操作')
    headers = mapped_column(JSON, comment='请求头')
    variables = mapped_column(JSON, comment='变量')
    validators = mapped_column(JSON, comment='断言规则')
    extracts = mapped_column(JSON, comment='提取')
    export = mapped_column(JSON, comment='输出')
    request = mapped_column(JSON, comment='请求参数')

    @classmethod
    async def get_list(cls, params: ApiQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.code:
            q.append(cls.code.like('%{}%'.format(params.code)))
        if params.module_ids:
            q.append(cls.module_id.in_(params.module_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.priority:
            q.append(cls.priority.in_(params.priority))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.api_status:
            q.append(cls.api_status == params.api_status)
        u = aliased(User)

        sort_type = 'asc' if params.sort_type == 0 else 'desc'

        if not params.order_field or params.order_field == 'creation_date':
            order_field = 'api_info.creation_date'
        elif params.order_field == 'updation_date':
            order_field = 'api_info.updation_date'
        elif params.order_field == 'name':
            order_field = 'api_info.name'
        elif params.order_field == 'project_name':
            order_field = 'project_info.name'
        elif params.order_field == 'module_name':
            order_field = 'module_info.name'
        elif params.order_field == 'created_by_name' or params.order_field == 'updated_by_name':
            order_field = 'user.nickname'
        else:
            order_field = 'api_info.id'
        order_by = f'{order_field} {sort_type}'

        stmt = select(cls.id,
                      cls.name,
                      cls.url,
                      cls.method,
                      cls.project_id,
                      cls.module_id,
                      cls.code_id,
                      cls.code,
                      cls.priority,
                      cls.status,
                      cls.tags,
                      cls.updated_by,
                      cls.created_by,
                      cls.updation_date,
                      cls.creation_date,
                      cls.enabled_flag,
                      ProjectDao.name.label('project_name'),
                      ModuleDao.name.label('module_name'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')).where(*q) \
            .outerjoin(ProjectDao, ProjectDao.id == cls.project_id) \
            .outerjoin(ModuleDao, ModuleDao.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .order_by(text(order_by))

        return await cls.pagination(stmt)

    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.enabled_flag == 1, cls.type == 1).all()

    @classmethod
    async def get_api_by_module_id(cls, module_id=None, module_ids=None):
        """查询模块是否有case关联"""
        q = [cls.enabled_flag == 1]
        if module_id:
            q.append(cls.module_id == module_id)
        if module_ids:
            q.append(cls.module_id.in_(module_ids))
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    def get_api_by_project_id(cls, project_id):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.enabled_flag == 1)

    @classmethod
    async def get_api_by_name(cls, name):
        """获取用例名是否存在"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1, cls.name == name)
        return await cls.get_result(stmt)

    @classmethod
    async def get_api_by_id(cls, id: int):
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')) \
            .where(cls.id == id, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_api_by_ids(cls, params: ApiIds):
        if not params.ids:
            return None
        stmt = select(cls.get_table_columns()).where(cls.id.in_(params.ids), cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_count_by_user_id(cls, user_id: typing.Any):
        """统计用户创建的用例数量"""
        stmt = select(func.count(cls.id).label('count')).where(cls.enabled_flag == 1,
                                                               cls.created_by == user_id)
        return await cls.get_result(stmt, first=True)

    @classmethod
    def get_api_by_time(cls, start_time, end_time):
        return cls.query.filter(cls.creation_date.between(start_time, end_time), cls.enabled_flag == 1)

    @classmethod
    def statistic_project_api_number(cls):
        return cls.query.outerjoin(ProjectDao, ProjectDao.id == cls.project_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(ProjectDao.name,
                           func.count(cls.id).label('case_num'),
                           User.username.label('employee_code'),
                           User.nickname.label('username'),
                           ) \
            .filter(cls.enabled_flag == 1)

    @classmethod
    def get_api_by_project_id_or_body(cls, project_id, body_name):
        """查询项目是否有case关联"""
        return cls.query.filter(cls.project_id == project_id, cls.request.like(('%{}%'.format(body_name))),
                                cls.enabled_flag == 1) \
            .with_entities(cls.id) \
            .all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()


class ApiCaseStep(Base):
    """步骤信息表"""
    __tablename__ = 'api_case_step'
    case_id = mapped_column(BigInteger, nullable=False, comment='用例id')
    source_id = mapped_column(BigInteger, nullable=False, comment='源id')
    name = mapped_column(String(255), nullable=False, comment="用例名称", index=True)
    project_id = mapped_column(BigInteger, nullable=False, comment='所属项目')
    module_id = mapped_column(BigInteger, nullable=False, comment='所属模块')
    status = mapped_column(Integer, comment='用例状态 10, 生效 ， 20 失效', default=10)
    code = mapped_column(String(255), comment='接口code')
    code_id = mapped_column(BigInteger, comment='关联接口id')
    priority = mapped_column(Integer, comment='优先级', default=3)
    url = mapped_column(String(255), nullable=False, comment='请求地址')
    method = mapped_column(String(255), comment='请求方式')
    tags = mapped_column(JSON, comment='用例标签')
    remarks = mapped_column(String(255), comment='描述')
    step_type = mapped_column(String(255), comment='描述')
    pre_steps = mapped_column(JSON, comment='前置步骤')
    post_steps = mapped_column(JSON, comment='后置步骤')
    setup_code = mapped_column(Text, comment='前置code')
    teardown_code = mapped_column(Text, comment='后置code')
    setup_hooks = mapped_column(JSON, comment='前置操作')
    teardown_hooks = mapped_column(JSON, comment='后置操作')
    headers = mapped_column(JSON, comment='请求头')
    variables = mapped_column(JSON, comment='变量')
    validators = mapped_column(JSON, comment='断言规则')
    extracts = mapped_column(JSON, comment='提取')
    export = mapped_column(JSON, comment='输出')
    request = mapped_column(JSON, comment='请求参数')
    step_id = mapped_column(BigInteger, comment='步骤id')
    parent_step_id = mapped_column(BigInteger, comment='父步骤id')
    index = mapped_column(String(255), comment='步骤顺序')
    node_id = mapped_column(String(255), comment='节点id')
    enable = mapped_column(Boolean, default=1, comment='是否启用 0 否 1 是')
    is_quotation = mapped_column(Integer, default=1, comment='是否引用 0 否 1 是')
    version = mapped_column(Integer, default=0, comment='版本号')

    @classmethod
    async def get_list(cls, params: ApiQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.code:
            q.append(cls.code.like('%{}%'.format(params.code)))
        if params.module_ids:
            q.append(cls.module_id.in_(params.module_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.created_by_name:
            q.append(User.nickname.like('%{}%'.format(params.created_by_name)))
        if params.priority:
            q.append(cls.priority.in_(params.priority))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.api_status:
            q.append(cls.api_status == params.api_status)
        u = aliased(User)

        sort_type = 'asc' if params.sort_type == 0 else 'desc'

        if not params.order_field or params.order_field == 'creation_date':
            order_field = 'api_info.creation_date'
        elif params.order_field == 'updation_date':
            order_field = 'api_info.updation_date'
        elif params.order_field == 'name':
            order_field = 'api_info.name'
        elif params.order_field == 'project_name':
            order_field = 'project_info.name'
        elif params.order_field == 'module_name':
            order_field = 'module_info.name'
        elif params.order_field == 'created_by_name' or params.order_field == 'updated_by_name':
            order_field = 'user.nickname'
        else:
            order_field = 'api_info.id'
        order_by = f'{order_field} {sort_type}'

        stmt = select(cls.id,
                      cls.name,
                      cls.url,
                      cls.method,
                      cls.project_id,
                      cls.module_id,
                      cls.code_id,
                      cls.code,
                      cls.priority,
                      cls.status,
                      cls.tags,
                      cls.updated_by,
                      cls.created_by,
                      cls.updation_date,
                      cls.creation_date,
                      cls.enabled_flag,
                      ProjectDao.name.label('project_name'),
                      ModuleDao.name.label('module_name'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')).where(*q) \
            .outerjoin(ProjectDao, ProjectDao.id == cls.project_id) \
            .outerjoin(ModuleDao, ModuleDao.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .order_by(text(order_by))

        return await cls.pagination(stmt)

    @classmethod
    async def get_step_by_case_id(cls, case_id: int, version: int):
        stmt = (select(cls.get_table_columns({"id"}),
                       ApiInfoDao.name.label('api_name'),
                       ApiInfoDao.method.label('api_method'),
                       )
                .outerjoin(ApiInfoDao, and_(ApiInfoDao.id == cls.source_id, ApiInfoDao.enabled_flag == 1))
                .where(cls.case_id == case_id,
                       cls.version == version,
                       cls.enabled_flag == 1).order_by(cls.index.asc()))
        return await cls.get_result(stmt)

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    async def get_relation_by_api_id(cls, api_id: typing.Union[str, int]):
        """获取关联关系，那些case 使用了对应的api"""
        q = [cls.enabled_flag == 1]
        stmt = select(
            func.any_value(cls.id.label("case_step_id")),
            func.any_value(ApiCase.id).label("id"),
            func.any_value(ApiCase.name).label("name"),
            func.any_value(func.concat('case_', ApiCase.id)).label("relation_id"),
            func.any_value(func.concat('api_', api_id)).label("from_relation_id"),
            func.any_value(func.concat('case_', ApiCase.id)).label("to_relation_id"),
            func.any_value(User.nickname).label("created_by_name"),
            ApiCase.creation_date,
        ) \
            .join(ApiCase, and_(cls.case_id == ApiCase.id,
                                cls.version == ApiCase.version,
                                ApiCase.enabled_flag == 1
                                )) \
            .outerjoin(User, User.id == ApiCase.created_by) \
            .where(*q, cls.source_id == api_id) \
            .group_by(ApiCase.id) \
            .order_by(ApiCase.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def get_relation_by_case_ids(cls, case_ids: typing.List[typing.Union[str, int]]):
        """获取关联关系，那些case 使用了对应的api"""
        q = [cls.enabled_flag == 1]
        stmt = select(
            func.any_value(cls.id.label("case_step_id")),
            func.any_value(ApiInfoDao.id).label("id"),
            func.any_value(func.concat('api_', ApiInfoDao.id)).label("relation_id"),
            func.any_value(func.concat('api_', ApiInfoDao.id)).label("from_relation_id"),
            func.any_value(func.concat('case_', ApiCase.id)).label("to_relation_id"),
            func.any_value(ApiInfoDao.name).label("name"),
            func.any_value(ApiInfoDao.creation_date).label("creation_date"),
            func.any_value(User.nickname).label("created_by_name"),
            func.any_value(ApiCase.creation_date),
        ) \
            .join(ApiCase, and_(cls.case_id == ApiCase.id,
                                cls.version == ApiCase.version,
                                ApiCase.enabled_flag == 1
                                )) \
            .outerjoin(User, User.id == ApiCase.created_by) \
            .outerjoin(ApiInfoDao, ApiInfoDao.id == cls.source_id) \
            .where(*q, cls.case_id.in_(case_ids), cls.step_type == 'api')
        return await cls.get_result(stmt)


class ApiCase(Base):
    """测试用例，集合"""
    __tablename__ = 'api_case'

    name = mapped_column(String(64), nullable=False, comment='名称', index=True)
    project_id = mapped_column(BigInteger, nullable=False, comment='所属项目')
    remarks = mapped_column(String(255), comment='备注')
    headers = mapped_column(JSON, comment='场景请求头')
    variables = mapped_column(JSON, comment='场景变量')
    step_data = mapped_column(JSON, comment='场景步骤')
    step_rely = mapped_column(Integer, comment='步骤依赖  1依赖， 0 不依赖')
    version = mapped_column(Integer(), comment='版本', default=0)

    # todo 目前步骤详情都冗余在单表，后面会拆为独立的表管理

    @classmethod
    async def get_list(cls, params: ApiCaseQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.created_by:
            q.append(User.nickname.like(f'%{params.created_by}%'))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.created_by_name:
            q.append(User.nickname.like(f'%{params.created_by_name}%'))
        if params.ids:
            q.append(cls.id.in_(params.ids))
        u = aliased(User)

        stmt = select(cls.id,
                      cls.name,
                      cls.project_id,
                      cls.remarks,
                      cls.created_by,
                      cls.creation_date,
                      cls.updated_by,
                      cls.updation_date,
                      cls.enabled_flag,
                      func.count(distinct(ApiCaseStep.id)).label('step_count'),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name'),
                      ProjectDao.name.label('project_name')).where(*q) \
            .outerjoin(ApiCaseStep, and_(ApiCaseStep.case_id == cls.id, cls.version == ApiCaseStep.version,
                                         ApiCaseStep.parent_step_id.is_(None))) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectDao, cls.project_id == ProjectDao.id) \
            .group_by(cls.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_api_by_id(cls, id: int):
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      User.nickname.label('created_by_name'),
                      u.nickname.label('updated_by_name')) \
            .where(cls.id == id, cls.enabled_flag == 1) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(u, u.id == cls.updated_by)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_case_by_ids(cls, ids: typing.List[int]):
        """根据套件ids查询用例"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_case_by_name(cls, name: str):
        """根据套件名称查询用例"""
        stmt = select(cls.get_table_columns()).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def get_count_by_user_id(cls, user_id: typing.Any):
        """统计用户创建的用例数量"""
        stmt = select(func.count(cls.id).label('count')).where(cls.enabled_flag == 1,
                                                               cls.created_by == user_id)
        return await cls.get_result(stmt, first=True)

    @classmethod
    def statistic_project_case_number(cls):
        """统计项目用例数量"""
        return cls.query.outerjoin(ProjectDao, ProjectDao.id == cls.project_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .with_entities(ProjectDao.name,
                           func.count(cls.id).label('case_num'),
                           User.username.label('employee_code'),
                           User.nickname.label('username'),
                           ) \
            .filter(cls.enabled_flag == 1)
