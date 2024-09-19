# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :UsersService.py
# @Time      :2024/9/13 21:19
# @Author    :XiaoQi
from common.enum.code_enum import CodeEnum
from apps.systems.dao.RoleDao import User
from apps.systems.model.RoleModel import UserIn


class UsersService:

    @staticmethod
    async def register(params: UserIn)->User :
        """
        用户注册
        :param params:
        :return:
        """
        Isregister = await User.get_user_by_name(params.name)
        if Isregister:
            return ValueError(CodeEnum.USERNAME_OR_EMAIL_IS_REGISTER.msg)
        user = await  User.create(params.dict())
        return user
