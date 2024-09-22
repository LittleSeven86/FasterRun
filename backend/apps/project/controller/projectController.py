# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :projectController.py
# @Time      :2024/9/11 21:22
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.project.dao.projectDao import ProjectDao
from apps.project.model.projectModel import ProjectQuery
from common.response.http_response import parter_success

router = APIRouter()

@router.post("/list",description="项目列表")
async def list(params: ProjectQuery):
    data = await ProjectDao.get_list(params)
    return parter_success(data)



