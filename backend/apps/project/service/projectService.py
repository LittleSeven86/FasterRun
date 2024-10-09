# coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :projectService.py
# @Time      :2024/9/10 19:55
# @Author    :XiaoQi
from apps.module.dao.moduleDao import ModuleDao
from apps.project.model.projectModel import *
from apps.project.dao.projectDao import *
from common.enum.code_enum import CodeEnum
from common.exception.BaseException import ParameterError


class ProjectService:

    @staticmethod
    async def list(param: ProjectQuery) -> typing.Dict:
        """
        获取项目列表
        :param param:
        :return:
        """
        result = await ProjectDao.get_list(param)
        return result

    @staticmethod
    async def get_all() -> typing.Dict:
        """
        获取项目列表
        :return:
        """
        data = await ProjectDao.get_all()
        return data

    @staticmethod
    async def save_or_update(params: ProjectModel) -> typing.Dict:
        """
        更新保存项目
        :param params:
        :return:
        """
        if params.id:
            project_info = await ProjectDao.get(params.id)
            if project_info.name != params.name:
                if await ProjectDao.get_project_by_name(params.name):
                    raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)
        else:
            if await ProjectDao.get_project_by_name(params.name):
                raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)

        return await ProjectDao.create_or_update(params.dict())

    @staticmethod
    async def deleted(params: ProjectId) -> int:
        """
        删除项目
        :param params:
        :return:
        """
        relation_module = await ModuleDao.get_module_by_project_id(params.id)
        if relation_module:
            raise ParameterError(CodeEnum.PROJECT_HAS_MODULE_ASSOCIATION)
        return await ProjectDao.delete(params.id)

    @staticmethod
    async def get_project_tree() -> typing.List:
        project_list = await ProjectDao.get_all()
        module_list = await ModuleDao.get_all()

        project_tree_list = []

        for project in project_list:
            project["children"] = []
            project["disabled"] = True
            if module_list:
                for module in module_list:
                    if module["project_id"] == project["id"]:
                        project["children"].append(module)
                        project["disabled"] = False
            project_tree_list.append(project)
        return project_tree_list