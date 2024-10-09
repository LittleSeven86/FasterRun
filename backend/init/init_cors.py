# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :init_cors.py
# @Time      :2024/10/9 19:34
# @Author    :XiaoQi
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.Config import config


def init_cors(app: FastAPI):
    """ 跨域请求 -- https://fastapi.tiangolo.com/zh/tutorial/cors/ """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )