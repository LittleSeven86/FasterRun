# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :api_router.py
# @Time      :2024/9/19 21:05
# @Author    :XiaoQi
from apps.project.controller import projectController
from apps.systems.controller import userController,menuController,roleController
from apps.module.controller import moduleController
from apps.api_info.controller import apiController
from apps.env.controller import sourceController,envController
from fastapi import APIRouter

api_router = APIRouter()


# project
api_router.include_router(projectController.router, prefix="/project", tags=["project"])

# systems
api_router.include_router(userController.router, prefix="/user", tags=["user"])
api_router.include_router(menuController.router, prefix="/menu", tags=["menu"])
api_router.include_router(roleController.router, prefix="/role", tags=["role"])

# module
api_router.include_router(moduleController.router, prefix="/module", tags=["module"])

# case
api_router.include_router(apiController.router, prefix="/api_info", tags=["api_info"])

# env
api_router.include_router(sourceController.router, prefix="/source", tags=["source"])
api_router.include_router(envController.router, prefix="/env", tags=["env"])