from fastapi import APIRouter

from apps.ui.model.ui_report import UiReportQuery, UiReportId, UiReportDetailQuery
from apps.ui.service.ui_report import UiReportService
from common.response.http_response import parter_success

router = APIRouter()


@router.post('/list', description="测试报告列表")
async def report_list(params: UiReportQuery):
    data = await UiReportService.list(params)
    return parter_success(data=data)


@router.post('/deleted', description="删除报告")
async def deleted(params: UiReportId):
    """
    删除报告
    :return:
    """
    data = await UiReportService.deleted(params)
    return parter_success(data)


@router.post('/getUiReportDetail', description="测试报告")
async def get_report_detail(params: UiReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await UiReportService.detail(params)
    return parter_success(data)


@router.post('/getUiReportStatistics', description="测试报告统计")
async def get_report_statistics(params: UiReportDetailQuery):
    """
    测试报告
    :return:
    """
    data = await UiReportService.statistics(params)
    return parter_success(data)
