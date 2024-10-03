# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :taskController.py
# @Time      :2024/10/3 09:24
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.tasks.model.taskModel import TimedTasksQuerySchema, TimedTasksInSchema, TimedTasksId, TimedTaskCaseQuery, \
    CrontabSaveSchema
from apps.tasks.model.taskRecordModel import TaskRecordQuery
from apps.tasks.service.TaskRecordServer import TaskRecordServer
from apps.tasks.service.taskService import TimedTasksService, CrontabService
from common.response.http_response import parter_success
from db.session import provide_async_session_router

router = APIRouter()


@router.post('/asnc_list', description="异步任务列表")
async def project_list(params: TaskRecordQuery):
    data = await TaskRecordServer.list(params)
    return parter_success(data)

@router.get("/{id}",description="根据id查询任务详情")
async def project_get(id: int):
    data = await TaskRecordServer.get_task_record_by_id(int(id))
    return parter_success(data)

@router.post('/job_list', description="定时任务列表")
async def timed_tasks_list(params: TimedTasksQuerySchema):
    data = await TimedTasksService.list(params)
    return parter_success(data)


@router.post('/saveOrUpdate', description="新增，修改定时任务")
@provide_async_session_router
async def save_or_update(params: TimedTasksInSchema):
    data = await TimedTasksService.save_or_update(params)
    return parter_success(data)


@router.post('/taskSwitch', description="定时任务开关")
async def task_switch(params: TimedTasksId):
    raise RuntimeError("验收环境关闭该功能，可以手都执行查看效果😊")
    data = await TimedTasksService.task_switch(params)
    return partner_success(data)


@router.post('/deleted', description="删除任务定时任务")
async def deleted_tasks(params: TimedTasksId):
    data = await TimedTasksService.deleted(params)
    return parter_success(data)


@router.post('/checkCrontab', description="定时任务校验crontab")
async def check_crontab(params: CrontabSaveSchema):
    data = await CrontabService.check_crontab(params.crontab)
    return parter_success(data)


@router.post('/runOnceJob', description="定时任务运行一次任务")
async def run_once_job(params: TimedTasksId):
    data = await TimedTasksService.run_once_job(params)
    return parter_success(data)


@router.post('/getTaskCaseInfo', description="获取定时任务关联case")
async def get_task_case_info(params: TimedTaskCaseQuery):
    data = await TimedTasksService.get_task_case_info(params)
    return parter_success(data)
