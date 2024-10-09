# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :reportController.py
# @Time      :2024/10/3 14:15
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.report.model.reportModel import TestReportQuery, TestReportId, TestReportDetailQuery
from apps.report.service.reportService import ReportService
from common.response.http_response import parter_success

router = APIRouter()

@router.post('/list', description="测试报告列表")
async def report_list(params: TestReportQuery):
    data = await ReportService.list(params)
    return parter_success(data=data)


@router.post('/deleted', description="删除报告")
async def deleted(params: TestReportId):
    """
    删除报告
    :return:
    """
    data = await ReportService.deleted(params)
    return parter_success(data)


@router.post('/getReportDetail', description="测试报告")
async def get_report_detail(params: TestReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await ReportService.detail(params)
    return parter_success(data)


@router.post('/getReportStatistics', description="测试报告统计")
async def get_report_statistics(params: TestReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await ReportService.statistics(params)
    return parter_success(data)