# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :idController.py
# @Time      :2024/10/8 19:37
# @Author    :XiaoQi

from fastapi import APIRouter

from common.response.http_response import parter_success
from common.utils.snowflake import IDCenter

router = APIRouter()


@router.get('/getId')
def get_id():
    """
    获取id
    :return:
    """
    data = IDCenter.get_id()
    return parter_success(str(data))