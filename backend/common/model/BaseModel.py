# coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :BaseModel.py
# @Time      :2024/9/10 19:44
# @Author    :XiaoQi

from pydantic import BaseModel
from pydantic.v1 import validator


class BaseSchema(BaseModel):
    def dict(self, *args, **kwargs):
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        return super(BaseSchema, self).dict(*args, **kwargs)

    @validator('*', pre=True)
    def blank_strings(cls, v):
        if v == "":
            return None
        return v
