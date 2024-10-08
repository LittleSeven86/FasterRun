# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :fileDao.py
# @Time      :2024/10/3 13:40
# @Author    :XiaoQi
from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from common.dao.base import Base


class FileInfo(Base):
    """文件信息"""
    __tablename__ = 'file_info'
    id = mapped_column(String(60), primary_key=True, autoincrement=False)
    name = mapped_column(String(255), comment='存储的文件名')
    file_path = mapped_column(String(255), comment='文件路径')
    extend_name = mapped_column(String(255), comment='扩展名称', index=True)
    original_name = mapped_column(String(255), comment='原名称')
    content_type = mapped_column(String(255), comment='文件类型')
    file_size = mapped_column(String(255), comment='文件大小')
