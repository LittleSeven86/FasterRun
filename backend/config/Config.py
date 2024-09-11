# coding=utf-8
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Config.py
# @Time      :2024/9/11 20:49
# @Author    :XiaoQi
import os
from os.path import abspath

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




    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Configs()
