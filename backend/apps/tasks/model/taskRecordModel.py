# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :taskRecordModel.py
# @Time      :2024/9/23 21:43
# @Author    :XiaoQi
import typing
from datetime import datetime

from common.model.BaseModel import BaseModel
from pydantic import Field


class TaskRecordQuery(BaseModel):
    task_name: str = Field(None, description="任务名称")
    task_id: str = Field(None, description="任务ID")
    trace_id: str = Field(None, description="trace_id")
    status: str = Field(None, description="任务状态")
    start_time: str = Field(None, description="任务开始时间")
    end_time: str = Field(None, description="任务结束时间")
    task_type: typing.Union[str, int] = Field(None, description="任务类型 10普通任务 20定时任务")
    business_id: typing.Union[str, int] = Field(None, description="业务id")


class TaskRecordIn(BaseModel):
    id: int = Field(None, description="")
    task_name: str = Field(None, description="任务名称")
    task_id: str = Field(None, description="任务ID")
    status: str = Field(None, description="任务状态")
    start_time: typing.Union[str, datetime] = Field(None, description="任务开始时间")
    end_time: typing.Union[str, datetime] = Field(None, description="任务结束时间")
    task_type: typing.Union[str, int] = Field(None, description="任务类型 10普通任务 20定时任务")
    business_id: str = Field(None, description="业务id")
    result: str = Field(None, description="任务结果")
    duration: str = Field(None, description="耗时")
    traceback: str = Field(None, description="异常信息")
    args: str = Field(None, description="任务参数")
    kwargs: str = Field(None, description="任务参数")
