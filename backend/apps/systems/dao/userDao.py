# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :userDao.py
# @Time      :2024/9/12 21:47
# @Author    :XiaoQi
import typing

from sqlalchemy import String, Text, JSON, Integer, select, Index, DateTime
from sqlalchemy.orm import mapped_column, aliased

from apps.systems.model.UserModel import UserLoginRecordQuery
from common.dao.base import Base
from apps.systems.model import RoleModel


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

class UserLoginRecord(Base):
    __tablename__ = "user_login_record"
    __table_args__ = (
        Index('idx_login_record_code_logintime', 'code', 'login_time'),
    )

    token = mapped_column(String(40), index=True, comment='登陆token')
    code = mapped_column(String(64), index=True, comment='账号')
    user_id = mapped_column(Integer, comment='用户id')
    user_name = mapped_column(String(50), comment='用户名称')
    logout_type = mapped_column(String(50), comment='退出类型')
    login_type = mapped_column(String(50), index=True, comment='登陆方式   扫码  账号密码等')
    login_time = mapped_column(DateTime, index=True, comment='登陆时间')
    logout_time = mapped_column(DateTime, comment='退出时间')
    login_ip = mapped_column(String(30), index=True, comment='登录IP')
    ret_msg = mapped_column(String(255), comment='返回信息')
    ret_code = mapped_column(String(9), index=True, comment='是否登陆成功  返回状态码  0成功')
    address = mapped_column(String(255), comment='地址')
    source_type = mapped_column(String(255), comment='来源')

    @classmethod
    async def get_list(cls, params: UserLoginRecordQuery):
        q = [cls.enabled_flag == 1]
        if params.token:
            q.append(cls.token.like('%{}%'.format(params.token)))
        if params.code:
            q.append(cls.code.like('%{}%'.format(params.code)))
        if params.user_name:
            q.append(cls.user_name.like('%{}%'.format(params.user_name)))
        u = aliased(User)
        stmt = select(cls) \
            .where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)
