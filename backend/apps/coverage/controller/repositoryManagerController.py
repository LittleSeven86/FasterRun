# from fastapi import APIRouter
#
# from apps.coverage.model.repositoryManagerModel import RepositoryListQuery
# # from apps.coverage.service.repositoryManagerService import RepositoryManagerService
# from common.response.http_response import parter_success
#
# router = APIRouter()
#
#
# @router.post('/getRepositoryList', description="获取仓库列表")
# async def get_repository_list(params: RepositoryListQuery):
#     data = await RepositoryManagerService.get_projects(params)
#     return parter_success(data)
#
#
# @router.post('/getBranches', description="获取仓库分支")
# async def get_repository_list(params: RepositoryListQuery):
#     data = await RepositoryManagerService.get_branches(params)
#     return parter_success(data)
