# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :init_router.py
# @Time      :2024/9/15 14:46
# @Author    :XiaoQi
from fastapi import FastAPI
from apps.api_router import api_router

from config.Config import config


def init_router(app:FastAPI):
    """
    注册路由
    :param app:
    :return:
    """
    app.include_router(api_router,prefix=config.API_PREFIX)