# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :relationGraphController.py
# @Time      :2024/10/8 20:04
# @Author    :XiaoQi
from fastapi import APIRouter

from apps.relation_graph.model.relationiGraphModel import RelationIn, RelationGraphService
from common.response.http_response import parter_success

router = APIRouter()


@router.post('/getRelationGraph', description="关系图")
async def api_case_list(params: RelationIn):
    data = await RelationGraphService.get_relation(params)
    return parter_success(data)
