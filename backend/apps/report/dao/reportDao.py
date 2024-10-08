# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :reportDao.py
# @Time      :2024/10/3 09:56
# @Author    :XiaoQi
from sqlalchemy import String, DateTime, Integer, Text, BigInteger, select, func, text, JSON, DECIMAL, and_
from sqlalchemy.orm import mapped_column

from apps.api_info.dao.apiInfoDao import ApiInfoDao
from apps.project.dao.projectDao import ProjectDao
from apps.report.model.reportModel import TestReportQuery, TestReportDetailQuery
from apps.systems.dao.userDao import User
from common.dao.base import Base


class ApiTestReport(Base):
    """报告表"""
    __tablename__ = 'api_test_report'

    name = mapped_column(String(255), nullable=False, comment='报告名称', index=True)
    start_time = mapped_column(DateTime, comment='执行时间')
    duration = mapped_column(String(255), comment='运行耗时')
    case_id = mapped_column(Integer, comment='执行用例id')
    run_mode = mapped_column(String(255), comment='运行模式， api 接口， case 用例')
    run_type = mapped_column(Integer, comment='运行类型， 10 同步， 20 异步，30 定时任务')
    success = mapped_column(Integer, comment='是否成功， True, False')
    run_count = mapped_column(Integer, comment='运行步骤数')
    actual_run_count = mapped_column(Integer, comment='实际步骤数')
    run_success_count = mapped_column(Integer, comment='运行成功数')
    run_fail_count = mapped_column(Integer, comment='运行失败数')
    run_skip_count = mapped_column(Integer, comment='运行跳过数')
    run_err_count = mapped_column(Integer, comment='运行错误数')
    run_log = mapped_column(Text, comment='运行日志')
    project_id = mapped_column(BigInteger, comment='项目id')
    module_id = mapped_column(BigInteger, comment='模块id')
    env_id = mapped_column(Integer, comment='运行环境')
    exec_user_id = mapped_column(Integer, comment='执行人id')
    exec_user_name = mapped_column(String(255), comment='执行人昵称')
    error_msg = mapped_column(Text, comment='错误信息')

    @classmethod
    async def get_list(cls, params: TestReportQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.user_ids:
            q.append(cls.execute_user_id.in_(params.user_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
        if params.min_and_max:
            q.append(cls.creation_date.between(*params.min_and_max))
        if params.exec_user_name:
            q.append(cls.exec_user_name.like('%{}%'.format(params.exec_user_name)))
        if params.case_id:
            q.append(cls.case_id == params.case_id)
        stmt = (select(cls.get_table_columns(exclude={"duration"}),
                       func.round(cls.duration, 2).label("duration"))
                .where(*q).order_by(cls.id.desc()))
        return await cls.pagination(stmt)

    @classmethod
    def get_project_by_name(cls, project_name):
        return cls.query.filter(cls.project_name == project_name, cls.enabled_flag == 1).first()

    @classmethod
    def get_report_by_id(cls, report_id):
        return cls.query.filter(cls.id == report_id, cls.enabled_flag == 1).first()

    @classmethod
    def get_report_by_time(cls, begin_time, end_time):
        return cls.query.filter(cls.enabled_flag == 1, cls.start_at.between(begin_time, end_time),
                                cls.success.isnot(None)) \
            .with_entities(cls.id,
                           cls.name,
                           cls.start_time,
                           cls.success,
                           cls.run_count,
                           cls.run_success_count,
                           cls.created_by,
                           cls.run_type,
                           cls.run_mode)

    @classmethod
    def statistic_report(cls, start_time=None, end_time=None):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        return cls.query.outerjoin(User, User.id == cls.execute_user_id) \
            .with_entities(
            func.count(cls.id).label('run_num'),
            User.username.label('employee_code'),
            User.nickname.label('username'),
        ) \
            .filter(cls.enabled_flag == 1,
                    cls.execute_user_id != -1,
                    *q)

    @classmethod
    def get_statistic_report(cls, start_time=None, end_time=None):
        q = []
        if start_time and end_time:
            q.append(cls.creation_date.between(start_time, end_time))
        return cls.query.filter(cls.enabled_flag == 1,
                                cls.execute_user_id != -1,
                                *q) \
            .outerjoin(ProjectDao, ProjectDao.id == cls.project_id) \
            .with_entities(
            cls.id,
            ProjectDao.name.label('project_name'),
            func.round(func.sum(func.if_(cls.success, 1, 0)) / func.count(cls.id) * 100, 2).label(
                'pass_rate'),
            func.round(func.sum(cls.successful_use_case) / func.sum(cls.run_test_count) * 100, 2).label(
                'successes_rate'),
        ).group_by(text('project_name'))


class ApiTestReportDetail:
    """报告表"""
    _mapper = {}

    @staticmethod
    def model(id: int):
        # 目前一个表，多个表修改取模数
        table_index = id % 1
        class_name = f'api_test_report_detail_{table_index}'

        mode_class = ApiTestReportDetail._mapper.get(class_name, None)
        if mode_class is None:
            class ModelClass(Base):
                __module__ = __name__
                __name__ = class_name,
                __tablename__ = class_name

                name = mapped_column(String(255), nullable=False, comment='步骤名称', index=True)
                case_id = mapped_column(String(255), comment='用例id')
                success = mapped_column(Integer, comment='是否成功， True, False')
                status = mapped_column(String(255),
                                       comment='步骤状态  success 成功  fail 失败  skip 跳过')
                step_id = mapped_column(String(255), comment='步骤id')
                parent_step_id = mapped_column(String(255), comment='父级步骤id')
                step_type = mapped_column(String(255), comment='步骤类型')
                step_tag = mapped_column(String(255),
                                         comment='步骤标签 pre 前置，post 后置，controller 控制器')
                message = mapped_column(Text, comment='步骤信息')
                variables = mapped_column(JSON, comment='步骤变量')
                env_variables = mapped_column(JSON, comment='环境变量')
                case_variables = mapped_column(JSON, comment='会话变量')
                session_data = mapped_column(JSON, comment='请求会话数据')
                export_vars = mapped_column(JSON, comment='导出变量')
                report_id = mapped_column(Integer, comment='报告id', index=True)
                url = mapped_column(String(255), comment='请求地址')
                method = mapped_column(String(255), comment='请求方法')
                start_time = mapped_column(DateTime, comment='开始时间')
                duration = mapped_column(DECIMAL(), comment='耗时')
                pre_hook_data = mapped_column(JSON, comment='前置步骤')
                post_hook_data = mapped_column(JSON, comment='后置步骤')
                setup_hook_results = mapped_column(JSON, comment='前置hook结果')
                teardown_hook_results = mapped_column(JSON, comment='后置hook结果')
                index = mapped_column(String(255), comment='顺序')
                status_code = mapped_column(Integer, comment='顺序')
                response_time_ms = mapped_column(DECIMAL(), comment='响应耗时')
                elapsed_ms = mapped_column(DECIMAL(), comment='请求耗时')
                log = mapped_column(Text, comment='运行日志')
                exec_user_id = mapped_column(Integer, comment='执行人id')
                exec_user_name = mapped_column(String(255), comment='执行人昵称')
                source_id = mapped_column(BigInteger, comment='源id')

                @classmethod
                async def get_list(cls, params: TestReportDetailQuery):
                    q = [cls.enabled_flag == 1]
                    q.append(cls.report_id == params.id)
                    if params.name:
                        q.append(cls.name.like(f"%{params.name}%"))
                    if params.url:
                        q.append(cls.url.like(f"%{params.url}%"))
                    if params.api_name:
                        q.append(ApiInfoDao.name.like(f"%{params.api_name}%"))
                    if params.step_type:
                        q.append(cls.step_type == params.step_type)
                    if params.status_list:
                        q.append(cls.status.in_(params.status_list))
                    if params.parent_step_id:
                        q.append(cls.parent_step_id == params.parent_step_id)
                    # else:
                    #     q.append(cls.parent_step_id == None)

                    stmt = select(cls.get_table_columns(),
                                  func.if_(ApiTestReport.run_type != 'api', ApiTestReport.name.label("case_name"),
                                           None),
                                  ApiInfoDao.name.label("api_name"),
                                  ApiInfoDao.created_by.label('api_created_by'),
                                  User.nickname.label('api_created_by_name'), ).where(*q) \
                        .outerjoin(ApiInfoDao, ApiInfoDao.id == cls.source_id) \
                        .outerjoin(ApiTestReport, ApiTestReport.id == cls.report_id) \
                        .outerjoin(User, User.id == ApiInfoDao.created_by) \
                        .order_by(cls.index)
                    return await cls.pagination(stmt)

                @classmethod
                async def statistics(cls, params: TestReportDetailQuery):
                    q = [cls.enabled_flag == 1, cls.report_id == params.id]
                    if params.parent_step_id:
                        q.append(cls.parent_step_id == params.parent_step_id)

                    sub_stmt = (select(
                        # 用例
                        # 用例步骤成功数
                        cls.case_id.label("case_id"),
                        func.count(func.if_(cls.case_id.is_not(None), 1, None)).label("case_count_1"),
                        func.sum(func.if_(and_(cls.status == "SUCCESS", cls.case_id.is_not(None)), 1, 0)).label(
                            "case_step_success_count"),
                        # 用例步骤成功数
                        func.sum(func.if_(and_(cls.status != "SUCCESS", cls.case_id.is_not(None)), 1, 0)).label(
                            "case_step_fail_count"),

                        # 步骤 -------------------------------------------------
                        # 总步骤数
                        func.count('*').label("step_count"),
                        func.count(func.if_(cls.status != "SKIP", 1, None)).label("effective_step_count"),
                        # 成功步骤数
                        func.sum(func.if_(and_(cls.status == "SUCCESS", cls.status != "SKIP"), 1, 0)).label(
                            "step_success_count"),
                        # 失败步骤数
                        func.sum(func.if_(cls.status == "FAILURE", 1, 0)).label(
                            "step_fail_count"),
                        # 跳过步骤数
                        func.sum(func.if_(cls.status == "SKIP", 1, 0)).label("step_skip_count"),

                        # 错误步骤数
                        func.sum(func.if_(cls.status == "ERROR", 1, 0)).label("step_error_count"),

                        # 平均请求时长
                        func.round(func.IFNULL(func.avg(cls.elapsed_ms), 0), 2).label("avg_request_time"),
                        # 总执行时长
                        func.sum(cls.duration).label("request_time_count"))
                                .where(*q).group_by(cls.case_id).subquery())

                    stmt = select(
                        func.count(func.if_(sub_stmt.c.case_id.is_not(None), 1, None)).label("case_count"),
                        func.sum(sub_stmt.c.step_count).label("step_count"),
                        func.round(func.avg(sub_stmt.c.avg_request_time), 2).label("avg_request_time"),
                        func.sum(sub_stmt.c.request_time_count).label("request_time_count"),

                        func.sum(
                            func.if_(and_(
                                sub_stmt.c.case_count_1 > 0,
                                sub_stmt.c.case_step_fail_count == 0), 1, 0))
                        .label("case_success_count"),

                        (func.count(func.if_(sub_stmt.c.case_id.is_not(None), 1, None)) - func.sum(
                            func.if_(and_(
                                sub_stmt.c.case_count_1 > 0,
                                sub_stmt.c.case_step_fail_count == 0), 1, 0))).label("case_fail_count"),

                        func.sum(sub_stmt.c.step_success_count).label("step_success_count"),
                        (func.sum(sub_stmt.c.step_fail_count)).label("step_fail_count"),
                        func.sum(sub_stmt.c.step_skip_count).label("step_skip_count"),
                        func.sum(sub_stmt.c.step_error_count).label("step_error_count"),
                        func.round(
                            func.sum(sub_stmt.c.step_success_count) / func.sum(sub_stmt.c.effective_step_count) * 100,
                            2).label("step_pass_rate"),
                        func.round(
                            (func.sum(func.if_(sub_stmt.c.case_step_fail_count == 0, 1, 0))) / func.count(
                                func.if_(sub_stmt.c.case_id.is_not(None), 1, None)) * 100,
                            2).label(
                            "case_pass_rate")
                    )

                    return await cls.get_result(stmt, first=True)

            mode_class = ModelClass
            ApiTestReportDetail._mapper[class_name] = ModelClass

        cls = mode_class()
        cls.id = id
        return cls