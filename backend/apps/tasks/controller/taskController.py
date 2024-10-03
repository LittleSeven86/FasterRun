# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :taskController.py
# @Time      :2024/10/3 09:24
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.tasks.model.taskRecordModel import TaskRecordQuery
from apps.tasks.service.TaskRecordServer import TaskRecordServer
from common.response.http_response import parter_success

router = APIRouter()


@router.post('/List', description="异步任务列表")
async def project_list(params: TaskRecordQuery):
    data = await TaskRecordServer.list(params)
    return parter_success(data)

@router.get("/{id}",description="根据id查询任务详情")
async def project_get(id: int):
    data = await TaskRecordServer.get_task_record_by_id(int(id))
    return parter_success(data)
