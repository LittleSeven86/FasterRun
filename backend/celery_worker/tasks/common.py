# -*- coding: utf-8 -*-
# @author: xiaobai
from apps.project.service.projectService import ProjectService
from celery_worker.worker import celery
from celery_worker.base import run_async
from apps.project.model.projectModel import ProjectModel


@celery.task
def add(i):
    return 1 + i


@celery.task
def save_project(params):
    data = ProjectModel(**params)
    run_async(ProjectService.save_or_update(data))
