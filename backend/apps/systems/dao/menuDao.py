# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :menuDao.py
# @Time      :2024/9/22 14:52
# @Author    :XiaoQi
import typing
from xml.etree.ElementInclude import include

from sqlalchemy import String, Integer, Boolean, select,update
from sqlalchemy.orm import mapped_column

from common.dao.base import Base


class Menu(Base):
    """菜单表"""
    __tablename__ = 'menu'

    path = mapped_column(String(255), nullable=False, comment='菜单路径')
    name = mapped_column(String(255), nullable=False, comment='菜单名称', index=True)
    component = mapped_column(Integer, comment='组件路径')
    title = mapped_column(String(255), comment='title', index=True)
    isLink = mapped_column(Boolean, comment='开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    linkUrl = mapped_column(String(255), comment='链接地址')
    isHide = mapped_column(Boolean, default=False, comment='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isKeepAlive = mapped_column(Boolean, default=True, comment='菜单是否缓存')
    isAffix = mapped_column(Boolean, default=False, comment='固定标签')
    isIframe = mapped_column(Boolean, default=False, comment='是否内嵌')
    roles = mapped_column(String(64), default=False, comment='权限')
    icon = mapped_column(String(64), comment='icon', index=True)
    parent_id = mapped_column(Integer, comment='父级菜单id')
    redirect = mapped_column(String(255), comment='重定向路由')
    sort = mapped_column(Integer, comment='排序')
    menu_type = mapped_column(Integer, comment='菜单类型')
    # lookup_id = mapped_column(Integer, comment='数据字典')
    active_menu = mapped_column(String(255), comment='显示页签')
    views = mapped_column(Integer, default=0, comment='访问数')

    @classmethod
    async def get_menu_by_ids(cls, ids: typing.List[int]):
        """获取菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_menu_all(cls):
        """获取菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_parent_id_by_ids(cls, ids: typing.List[int]):
        """根据子菜单id获取父级菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_parent_id_all(cls):
        """根据子菜单id获取父级菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_menu_by_title(cls, title: str):
        stmt = select(cls.get_table_columns()).where(cls.title == title, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_menu_by_name(cls, name: str):
        stmt = select(cls.get_table_columns()).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_menu_by_parent(cls, parent_id: int):
        stmt = select(cls.get_table_columns()) \
            .where(cls.parent_id == parent_id, cls.enabled_flag == 1) \
            .order_by(cls.sort)
        return await cls.get_result(stmt, True)

    @classmethod
    async def add_menu_views(cls, menu_id: int):
        all = select(cls.get_table_columns()).where(cls.id == menu_id, cls.enabled_flag == 1)
        stmt = update(cls.__table__)  \
            .where(cls.id == menu_id, cls.enabled_flag == 1)    \
            .values(views=cls.views+1)
        result = await cls.execute(stmt)
        return result.rowcount