# Source Generated with Decompyle++
# File: http_client.pyc (Python 3.11)

"""httpx client 工厂 — 对脏代理环境变量容错。

背景：Clash / v2rayN 等代理工具常把 ``NO_PROXY`` 写成
``127.0.0.1,localhost,::1,::1/128`` —— 裸 IPv6 条目（无方括号）会让
httpx 在 AsyncClient **构造时** 就抛 ``InvalidURL: Invalid port: ':1'``，
导致更新检查、游戏轮询等所有 httpx 调用集体失败。

策略：先按默认 trust_env=True 构造（尊重用户正常代理）；解析失败则
降级 trust_env=False（忽略环境变量）并记一次 warning。
"""
import httpx
from src.utils.logger import get_logger
logger = get_logger('System')
_warned_bad_proxy_env = False

def create_async_client(**kwargs):
    '''等价 httpx.AsyncClient(**kwargs)，但环境代理变量损坏时自动降级直连。'''
    pass
# WARNING: Decompyle incomplete

