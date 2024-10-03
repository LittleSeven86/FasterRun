# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Config.py
# @Time      :2024/9/11 20:49
# @Author    :XiaoQi
import os
import typing
from os.path import abspath
from pathlib import Path

from pydantic.v1 import BaseSettings, AnyUrl

project_banner = """
,------.               ,--.                ,------.                  
|  .---',--,--. ,---.,-'  '-. ,---. ,--.--.|  .--. ',--.,--.,--,--,  
|  `--,' ,-.  |(  .-''-.  .-'| .-. :|  .--'|  '--'.'|  ||  ||      \ 
|  |`  \ '-'  |.-'  `) |  |  \   --.|  |   |  |\  \ '  ''  '|  ||  | 
`--'    `--`--'`----'  `--'   `----'`--'   `--' '--' `----' `--''--' 
"""

__version__ = "1.0"

project_desc = """
    🎉 FastRun 管理员接口汇总 🎉
"""

class Configs(BaseSettings):
    """
    项目配置
    """
    PROJECT_DESC: str = project_desc
    PROJECT_BANNER: str = project_banner
    PROJECT_VERSION: str = __version__
    BASE_URL:AnyUrl = "http://127.0.0.1:8100"  # 开发环境
    BASEDIR: str = os.path.join(abspath(os.path.dirname(os.path.abspath(__file__))))

    """
    日志配置
    """
    LOGGER_DIR: str = "logs"  # 日志文件夹名
    LOGGER_NAME: str = 'FastRun.log'  # 日志文件名  (时间格式 {time:YYYY-MM-DD_HH-mm-ss}.log)
    LOGGER_LEVEL: str = 'INFO'  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "10 MB"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "7 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]

    """
    数据库配置
    """
    # DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db?check_same_thread=False"  # Sqlite(异步)
    # DATABASE_URI: str = Field(..., env="MYSQL_DATABASE_URI")  # MySQL(异步)
    DATABASE_URI: str = "mysql+aiomysql://root:123456@localhost:3306/zerorunner"
    # DATABASE_URI: str = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres"  # PostgreSQL(异步)
    DATABASE_ECHO: bool = False  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)
    DATABASE_POOL_SIZE: int = 10    # 队列池个数
    MAX_OVERFLOW: int = 10       # 队列池最大溢出个数
    POOL_PRE_PING:bool = True       # 将启用连接池“预ping”功能，该功能在每次签出时测试连接的活跃度
    POOL_RECYCLE:int = 7200     # 2个小时回收线程


    # redis
    # REDIS_URI: str = Field(..., env="jdbc:redis://localhost:6379/0")  # redis
    REDIS_URI: str = "redis://localhost:6379/0"


    # api配置
    API_PREFIX: str = "/api"  # 接口前缀


    # 常量
    # 公共
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    DEFAULT_FAIL = -1

    # Cache Time
    CACHE_FIVE_SECONDS = 5
    CACHE_MINUTE = 60
    CACHE_THREE_MINUTE = 60 * 3
    CACHE_FIVE_MINUTE = 60 * 5
    CACHE_TEN_MINUTE = 60 * 10
    CACHE_HALF_HOUR = 60 * 30
    CACHE_HOUR = 60 * 60
    CACHE_THREE_HOUR = 60 * 60 * 3
    CACHE_TWELVE_HOUR = 60 * 60 * 12
    CACHE_DAY = 60 * 60 * 24
    CACHE_WEEK = 60 * 60 * 24 * 7
    CACHE_MONTH = 60 * 60 * 24 * 30

    # Cache
    TEST_USER_INFO = 'fastrun:user_token:{0}'  # 用户token缓存
    TEST_EXECUTE_SET = 'fastrun:test_execute_set:case:{}'  # 用例执行集合
    TEST_EXECUTE_STATS = 'fastrun:test_execute_set:stats:{}'  # 用例执行统计
    TEST_EXECUTE_TASK = 'fastrun:test_execute_set:task:{}'  # 运行任务数
    TEST_EXECUTE_PARAMETER = 'fastrun:test_execute_set:extract_parameter:{}'  # 变量
    DATA_STRUCTURE_CASE_UPDATE = 'fastrun:data_structure:user:{}'  # 数据构造用户变更的接口信息
    TEST_USER_LOGIN_TIME = 'fastrun:user_login_time:{}'  # 数据构造用户变更的接口信息

    # 性能
    PREFORMANCE_RUN_STATUS = 'performance_test:status'
    PREFORMANCE_FREE = 0
    PREFORMANCE_INIT = 10
    PREFORMANCE_BUSY = 20
    PREFORMANCE_ABORT = 30

    PREFORMANCE_CODE = 'code'
    PREFORMANCE_SIGN_CODE = 'sign_code'

    THREAD_MAXMUM = 100
    RUN_NUMBER_MAXMUM = 1000000
    DEBUG_MAXMUM = 100

    API_PREFIX: str = "/api"  # 接口前缀
    STATIC_DIR: str = 'static'  # 静态文件目录
    GLOBAL_ENCODING: str = 'utf8'  # 全局编码
    CORS_ORIGINS: typing.List[typing.Any] = ["*"]  # 跨域请求
    WHITE_ROUTER: list = ["/api/user/login", "/api/file","/api/user/register"]  # 路由白名单，不需要鉴权

    # celery worker
    # broker_url: str = Field(..., env="CELERY_BROKER_URL")
    broker_url: str = "pyamqp://admin:123456@localhost:5672"
    # result_backend: str = Field(..., env="CELERY_RESULT_BACKEND")
    task_serializer: str = "pickle"
    result_serializer: str = "pickle"
    accept_content: typing.Tuple = ("pickle", "json",)
    task_protocol: int = 2
    timezone: str = "Asia/Shanghai"
    enable_utc: bool = False
    broker_connection_retry_on_startup: bool = True
    # 并发工作进程/线程/绿色线程执行任务的数量 默认10
    worker_concurrency: int = 10
    # 一次预取多少消息乘以并发进程数 默认4
    worker_prefetch_multiplier: int = 4
    # 池工作进程在被新任务替换之前可以执行的最大任务数。默认是没有限制
    worker_max_tasks_per_child: int = 100
    # 连接池中可以打开的最大连接数 默认10
    broker_pool_limit: int = 10
    # 传递给底层传输的附加选项的字典。设置可见性超时的示例（Redis 和 SQS 传输支持）
    result_backend_transport_options: typing.Dict[str, typing.Any] = {'visibility_timeout': 3600}
    worker_cancel_long_running_tasks_on_connection_loss: bool = True
    include: typing.List[str] = [
        # 'celery_worker.tasks.test_case',
        'celery_worker.tasks.common',
        'celery_worker.tasks.task_run',
        # 'celery_worker.tasks.ui_case',
    ]
    # task_queues = (
    #     Queue('default', routing_key='default'),
    #     Queue('ui_case', routing_key='ui_case'),
    #     Queue('api_case', routing_key='api_case'),
    # )

    #  job -A your_app worker -Q api_case,ui_case

    TEST_FILES_DIR: str = Path(__file__).parent.joinpath("static", "files").as_posix()
    PROJECT_ROOT_DIR: str = Path(__file__).parent.as_posix()

    task_run_pool: int = 3

    # job beat
    # beat_db_uri: str = Field(..., env="CELERY_BEAT_DB_URL")
    beat_db_uri: str = ""


    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Configs()
