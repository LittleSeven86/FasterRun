from fastapi import APIRouter

from apps.lookup.model.lookupModel import LookupId, LookupValueQuery, LookupIn, LookupQuery, LookupValueIn
from apps.lookup.service.lookupService import LookupValueService, LookupService
from common.response.http_response import parter_success

router = APIRouter()


@router.post('/getAllLookup', description="获取所有数据字典")
async def get_all_lookup():
    data = await LookupValueService.get_all_lookup()
    return parter_success(data)


@router.post('/getLookupList', description="获取数据字典列表")
async def lookup_list(params: LookupQuery):
    data = await LookupService.list(params)
    return parter_success(data)


@router.post('/saveOrUpdateLookup', description="新增或更新字典")
async def save_or_update_lookup(params: LookupIn):
    data = await LookupService.save_or_update(params)
    return parter_success(data)


@router.post('/delLookup', description="删除字典")
async def del_lookup(params: LookupId):
    data = await LookupService.deleted(params)
    return parter_success(data)


@router.post('/getLookupValue', description="获取字典值")
async def get_lookup_value(params: LookupValueQuery):
    """获取字典值"""
    data = await LookupValueService.get_lookup_value(params)
    return parter_success(data)


@router.post('/saveOrUpdateLookupValue', description="保存或更新字典值")
async def save_or_update_lookup_value(params: LookupValueIn):
    """保存或更新字典值"""
    data = await LookupValueService.save_or_update(params)
    return parter_success(data)


@router.post('/delLookupValue', description="删除字典值")
async def del_lookup_value(params: LookupId):
    """删除字典值"""
    data = await LookupValueService.deleted(params)
    return parter_success(data)
