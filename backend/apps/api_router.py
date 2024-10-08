# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :api_router.py
# @Time      :2024/9/19 21:05
# @Author    :XiaoQi

from fastapi import APIRouter


# from autotest.apis.websocket import websocket
# from autotest.apis.websocket.ui import web_ui_case
# from autotest.apis.job import task_record

from apps.project.controller import projectController
from apps.module.controller import moduleController
from apps.api_info.controller import apiController
from apps.api_case.controller import apiCaseController
from apps.systems.controller import userController,roleController,menuController,fileController,idController
from apps.ui.controller import uiPageController,uiReportController,uiElementController,uiCaseController
from apps.lookup.controller import lookupController
from apps.report.controller import reportController
from apps.statistics.controller import statisticsController
from apps.env.controller import sourceController,envController
from apps.function.controller import funcController
from apps.tasks.controller import taskController
from apps.coverage.controller import coverageController,repositoryManagerController
from apps.relation_graph.controller import relationGraphController


app_router = APIRouter()

# api
app_router.include_router(projectController.router, prefix="/project", tags=["project"])
app_router.include_router(moduleController.router, prefix="/module", tags=["module"])
app_router.include_router(apiController.router, prefix="/apiInfo", tags=["apiInfo"])
app_router.include_router(apiCaseController.router, prefix="/apiCase", tags=["apiCase"])
app_router.include_router(reportController.router, prefix="/report", tags=["apiReport"])
app_router.include_router(sourceController.router, prefix="/dataSource", tags=["dataSource"])
app_router.include_router(funcController.router, prefix="/functions", tags=["functions"])
app_router.include_router(taskController.router, prefix="/timedTasks", tags=["TimedTasks"])
app_router.include_router(envController.router, prefix="/env", tags=["env"])
app_router.include_router(statisticsController.router, prefix="/statistics", tags=["statistics"])
app_router.include_router(relationGraphController.router, prefix="/relationGraph", tags=["relationGraph"])

# ui
app_router.include_router(uiPageController.router, prefix="/uiPage", tags=["uiPage"])
app_router.include_router(uiElementController.router, prefix="/uiElement", tags=["uiElement"])
app_router.include_router(uiCaseController.router, prefix="/uiCase", tags=["uiCase"])
app_router.include_router(uiReportController.router, prefix="/uiReport", tags=["uiReport"])

# system
app_router.include_router(userController.router, prefix="/user", tags=["user"])
app_router.include_router(menuController.router, prefix="/menu", tags=["menu"])
app_router.include_router(roleController.router, prefix="/roles", tags=["roles"])
app_router.include_router(lookupController.router, prefix="/lookup", tags=["lookup"])
app_router.include_router(idController.router, prefix="/idCenter", tags=["idCenter"])
app_router.include_router(fileController.router, prefix="/file", tags=["file"])

# coverage
# app_router.include_router(coverageController.router, prefix="/coverage/report", tags=["coverage"])
# app_router.include_router(repositoryManagerController.router, prefix="/coverage/repository", tags=["repository"])

# job
# app_router.include_router(task_record.router, prefix="/job", tags=["job"])

# # websocket
# app_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
# app_router.include_router(web_ui_case.router, prefix="/ws/uiCase", tags=["UIWebsocket"])
