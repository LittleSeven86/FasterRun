# coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ProjectService.py
# @Time      :2024/9/10 19:55
# @Author    :XiaoQi
import typing

import typing

from watchfiles import awatch

from common.enum.code_enum import CodeEnum
from common.exception.BaseException import ParameterError
from entity.ProjectInfoModel import *

class ProjectService:

    @staticmethod
    async def list(param: ProjectQuery) -> typing.Dict:
        """
        获取项目列表
        :param param:
        :return:
        """
        result = await ProjectIn
        return