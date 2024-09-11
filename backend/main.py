from fastapi import FastAPI

import uvicorn
import click

from config.Config import Configs, config

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
    pass


@app.on_event("startup")
async def startup() -> None:
    click.echo(config.PROJECT_BANNER)
    await init_app()


@app.on_event("shutdown")
async def shutdown() -> None:
    pass


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
