# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :serialize.py
# @Time      :2024/9/11 21:48
# @Author    :XiaoQi

import typing
from datetime import datetime
from json import JSONEncoder

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, select, func, literal_column, Row
from sqlalchemy.orm import noload, DeclarativeMeta
from sqlalchemy.testing.config import options

# 对 Select 或者Query的结果进行范型转换
T = typing.TypeVar("T",Select,"Query[Any]")

def count_query(query: Select) -> Select:
    """
    获取count sql
    :param query: sql
    :return:
    """
    count_subquery = typing.cast(
        typing.Any,query.order_by(None)).options(noload("*")).subquery()
    return select(
        func.count(literal_column("*"))).select_from(count_subquery)

def pagenate_query(query:T,page:int,page_size:int) -> T:
    return query.limit(page_size).offset(page_size * (page - 1))



def default_serialize(obj):

    def serialize_int(value):
        return str(value) if len(str(value)) > 15 else value

    def serialize_dict(d):
        return {key: default_serialize(value) for key, value in d.items()}

    def serialize_list(l):
        return [default_serialize(i) for i in l]

    def serialize_datetime(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def serialize_row(row):
        data = dict(zip(row._fields, row._data))
        return serialize_dict(data)

    def serialize_declarative(obj):
        return {c.name: default_serialize(getattr(obj, c.name)) for c in obj.__table__.columns}

    type_serializers = {
        int: serialize_int,
        dict: serialize_dict,
        list: serialize_list,
        datetime: serialize_datetime,
        Row: serialize_row,
        DeclarativeMeta: serialize_declarative,
        typing.Callable: repr
    }

    for data_type, serializer in type_serializers.items():
        if isinstance(obj, data_type):
            return serializer(obj)

    try:
        # 处理其他所有无法识别的数据类型
        return jsonable_encoder(obj)
    except TypeError:
        # 在无法序列化对象时返回其字符串表示形式
        return repr(obj)