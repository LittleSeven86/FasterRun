from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
import uvicorn
import click
from loguru import logger
from config.Config import Configs, config
from config.dependencies import login_verification
from init.init_cors import init_cors  # 这个需要直接调用来添加中间件
from init.init_logger import init_logger
from init.init_router import init_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await init_app()
    click.echo(config.PROJECT_BANNER)
    yield  # 这部分相当于允许请求处理的代码运行
    # Shutdown code
    pass

# 创建 FastAPI 实例
app = FastAPI(
    title="FastRun",
    description=config.PROJECT_DESC,
    version=config.PROJECT_VERSION,
    dependencies=[Depends(login_verification)],
    debug=True,
    lifespan=lifespan
)

# 在创建应用时立即添加中间件
init_cors(app)
init_logger()  # 也可以提前初始化日志

async def init_app() -> None:
    """
    初始化应用
    """
    init_router(app)  # 路由初始化在 lifespan 内进行即可

    logger.info("项目初始化成功")

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
