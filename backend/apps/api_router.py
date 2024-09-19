# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :api_router.py
# @Time      :2024/9/19 21:05
# @Author    :XiaoQi
from apps.project.controller import ProjectController
from apps.systems.controller import user_controller
from fastapi import APIRouter

api_router = APIRouter()


# project
api_router.include_router(ProjectController.router, prefix="/project", tags=["project"])

# systems
api_router.include_router(user_controller.router, prefix="/user", tags=["user"])

