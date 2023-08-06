# coding=utf-8
import sys

from pro.utils.util import get_ip
import os
"""
    此文件为启动的配置文件 不准瞎写
"""


# 服务器名称False
SERVICENAME = "promotion-service"

# Consul ip
CONSUL_HOST = "172.16.8.108"

# consul端口号
CONSUL_PORT = 8500

# 本机ip
_HOST = get_ip()



# 时分秒
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


