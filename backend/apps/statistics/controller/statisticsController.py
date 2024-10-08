# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :statisticsController.py
# @Time      :2024/10/8 20:01
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.statistics.service.statisticService import StatisticService
from common.response.http_response import parter_success

router = APIRouter()


@router.post("/personalStatistics", description="个人统计")
async def personal_statistics():
    data = await StatisticService.personal_statistics()
    return parter_success(data)