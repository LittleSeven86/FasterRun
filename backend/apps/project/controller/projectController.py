# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :projectController.py
# @Time      :2024/9/11 21:22
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.project.dao.projectDao import ProjectDao
from apps.project.model.projectModel import ProjectQuery, ProjectModel, ProjectId
from apps.project.service.projectService import ProjectService
from common.response.http_response import parter_success

router = APIRouter()

@router.post('/list', description="项目列表")
async def project_list(params: ProjectQuery):
    data = await ProjectService.list(params)
    return parter_success(data)


@router.post('/getAllProject', description="获取所有项目")
async def get_all_project():
    data = await ProjectService.get_all()
    return parter_success(data)


@router.post('/saveOrUpdate', description="更新保存项目")
async def save_or_update(params: ProjectModel):
    data = await ProjectService.save_or_update(params)
    return parter_success(data)


@router.post('/deleted', description="删除")
async def deleted(params: ProjectId):
    data = await ProjectService.deleted(params)
    return parter_success(data)


@router.post('/getProjectTree', description="获取项目树结构")
async def get_project_tree():
    """
    项目树结构
    :return:
    """
    data = await ProjectService.get_project_tree()
    return parter_success(data)


