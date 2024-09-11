# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Base.py
# @Time      :2024/9/10 20:06
# @Author    :XiaoQi
from typing import Union, Dict

from sqlalchemy import BigInteger, DateTime, func, Boolean, String, select
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, mapped_column


@as_declarative()
class Base:
    """
    基本表
    # db.scalar(sql) 返回的是标量(原始数据) <models.department.Department object at 0x000002F2C2D22110>
    # db.execute(sql) 返回的是元组 (<models.department.Department object at 0x000002F2C2D22110>)
    # db.scalars(sql).all()  [<models...>, <models...>, <models...>]
    # db.execute(sql).fetchall()  [(<models...>,), (<models...>,), (<models...>,)]
    """
    __name__: str  # 表名
    __table_args__ = {"mysql_charset": "utf8"}  # 设置表的字符集

    __mapper_args__ = {"eager_defaults": True}  # 防止 insert 插入后不刷新

    @declared_attr
    def __tablename__(cls) -> str:
        """将类名小写并转化为表名 __tablename__"""
        return cls.__name__.lower()

    # 设置表字段
    id = mapped_column(BigInteger(), nullable=False, primary_key=True, autoincrement=True, comment='主键')
    creation_date = mapped_column(DateTime(), default=func.now(), comment='创建时间')
    created_by = mapped_column(BigInteger, comment='创建人ID')
    updation_date = mapped_column(DateTime(), default=func.now(), onupdate=func.now(), comment='更新时间')
    updated_by = mapped_column(BigInteger, comment='更新人ID')
    enabled_flag = mapped_column(Boolean(), default=1, nullable=False, comment='是否删除, 0 删除 1 非删除')
    trace_id = mapped_column(String(255), comment="trace_id")

    @classmethod
    async def get(cls, id: Union[int, str], to_dict: object = False) -> Union["Base", Dict, None]:
        """
        根据id查询项目
        :param id: 项目id
        :param to_dict: 转字典
        :return: 项目信息
        """
        if not id or not isinstance(id, int):
            return None
        sql = select(cls).where(cls.id == id,cls.enabled_flag == 1)
        result = await cls.execute(sql)