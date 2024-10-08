import typing

from sqlalchemy import String, BigInteger, JSON, Integer, select, func, distinct, and_
from sqlalchemy.orm import mapped_column, aliased

from apps.api_case.model.apiCaseModel import ApiCaseQuery

from apps.project.dao.projectDao import ProjectDao
from apps.systems.dao.userDao import User
from common.dao.base import Base


class ApiCaseDao(Base):
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
        from apps.api_info.dao.apiInfoDao import ApiCaseStep
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