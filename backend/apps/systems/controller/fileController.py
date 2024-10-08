# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :fileController.py
# @Time      :2024/10/8 19:27
# @Author    :XiaoQi
from fastapi import APIRouter, UploadFile, File

from apps.systems.model.fileModel import FileId
from apps.systems.service.fileService import FileService
from common.response.http_response import parter_success

router = APIRouter()


@router.post('/upload', description="文件上传")
async def upload(file: UploadFile = File(...)):
    result = await FileService.upload(file)
    return parter_success(result)


@router.get('/download/{file_id}', description="文件下载")
async def download(file_id: str):
    result = await FileService.download(file_id)
    return result


@router.get('/getFileById', description="根据id获取文件下载地址")
async def get_file_by_id(params: FileId):
    return await FileService.get_file_by_id(params)


@router.post('/deleted', description="文件删除")
async def deleted(params: FileId):
    data = await FileService.get_file_by_id(params)
    return parter_success(data)