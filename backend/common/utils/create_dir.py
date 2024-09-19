# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :create_dir.py
# @Time      :2024/9/15 14:49
# @Author    :XiaoQi

from pathlib import Path


def create_dir(file_name: str) -> Path:
    """ 创建文件夹 """
    path = Path(file_name).absolute().parent / file_name  # 拼接日志文件夹的路径
    if not Path(path).exists():  # 文件是否存在
        Path.mkdir(path)

    return path