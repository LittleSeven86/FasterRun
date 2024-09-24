# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :moduleService.py
# @Time      :2024/9/22 22:24
# @Author    :XiaoQi
import typing
from curses.ascii import isblank

from apps.api_info.dao.apiInfoDao import ApiInfoDao
from apps.module.model.moduleModel import ModuleQuery, ModuleIn, ModuleId
from apps.module.dao.moduleDao import ModuleDao
from common.enum.code_enum import CodeEnum
from common.exception.BaseException import ParameterError


class ModuleService:
    """模块处理类"""

    @staticmethod
    async def list(params: ModuleQuery) -> typing.Dict:
        """
        获取模块列表
        :param params: 查询参数
        :return:
        """
        data = await ModuleDao.get_list(params)
        return data

    @staticmethod
    async def get_all() -> typing.Dict:
        """
        获取模块列表
        :return:
        """
        data = await ModuleDao.get_all()
        return data

    @staticmethod
    async def save_or_update(params: ModuleIn) -> typing.Dict:
        """
        模块保存方法
        :param params: 参数
        :return:
        """
        # 当模块关联的包发生变更时，原始包移除模块信息
        same_name_module = await ModuleDao.get_module_by_name(params.name)
        if params.id:
            module_info = await ModuleDao.get(params.id)
            if module_info.name != params.name:
                if await ModuleDao.get_module_by_name(params.name):
                    raise ParameterError(CodeEnum.MODULE_NAME_EXIST)
        else:
            if same_name_module:
                raise ParameterError(CodeEnum.MODULE_NAME_EXIST)
        return await ModuleDao.create_or_update(params.dict())

    @staticmethod
    async def get_byId(params: ModuleId):
        if not params:
            raise ParameterError(CodeEnum.MODULE_NOT_EXIST.msg)
        return await ModuleDao.get_module_info_byId(params)


    @staticmethod
    async def search_byName(params:str):
        return await ModuleDao.search_by_moduleName(params)


    @staticmethod
    async def deleted(params: ModuleId):
        """
        删除模块
        :param params:
        :return:
        """
        if params.id:
            relation_api = await ApiInfoDao.get_api_by_module_id(params.id)
            if relation_api:
                raise ParameterError(CodeEnum.MODULE_HAS_CASE_ASSOCIATION)
            return await ModuleDao.delete(params.id)


