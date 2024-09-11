# coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :BaseModel.py
# @Time      :2024/9/10 19:44
# @Author    :XiaoQi

from pydantic import BaseModel,validator
from common.constants.Constants import Constants


class BaseModel(BaseModel):

    def dict(self,*args,**kwargs):
        # 当调用 dict() 方法时，默认会排除值为 None 的字段
        if Constants.EXCLUDE_NONE not in kwargs:
            kwargs[Constants.EXCLUDE_NONE] = True
        return super(BaseModel,self).dict(*args,**kwargs)

    @validator("*",pre=True)
    def blank_strings(cls, values):
        if values is None:
            return None
        return values
