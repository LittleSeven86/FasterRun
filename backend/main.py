from fastapi import FastAPI

import uvicorn
import click
from loguru import logger

from config.Config import Configs, config
from init.init_logger import init_logger
from init.init_router import init_router

app = FastAPI(
    title="FastRun",
    description=config.PROJECT_DESC,
    version=config.PROJECT_VERSION,
    dependencies=[]
)


async def init_app() -> None:
    """
    注册中心
    :return:
    """
    init_router(app)
    init_logger()

    logger.info("项目初始化成功")



@app.on_event("startup")
async def startup() -> None:
    click.echo(config.PROJECT_BANNER)
    await init_app()


@app.on_event("shutdown")
async def shutdown() -> None:
    pass


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
