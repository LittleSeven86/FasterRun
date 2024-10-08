# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :coverageController.py
# @Time      :2024/10/8 19:50
# @Author    :XiaoQi

from fastapi import APIRouter, Body

from apps.coverage.model.coverageReportModel import JacocoReportIn, CoverageListQuery, CoverageReportQuery
from apps.coverage.service.coverageReportService import CoverageReportService
from common.response.http_response import parter_success

router = APIRouter()


@router.post('/coverageStart', description="开始覆盖率")
async def get_repository_list(params: JacocoReportIn):
    data = await CoverageReportService.start(params)
    return parter_success(data)


@router.post('/getReportList', description="获取报告详情")
async def get_report_detail(params: CoverageListQuery):
    data = await CoverageReportService.list(params)
    return parter_success(data)


@router.post('/getReportById', description="获取报告详情")
async def get_report_detail(body=Body(...)):
    data = await CoverageReportService.get(body.get("id", None))
    return parter_success(data)


@router.post('/getCoverageDetail', description="获取覆盖详情")
async def get_report_detail(params: CoverageReportQuery):
    data = await CoverageReportService.get_report_detail(params)
    return parter_success(data)