# Source Generated with Decompyle++
# File: websocket.pyc (Python 3.11)

'''WebSocket 连接管理'''
import asyncio
import json
from fastapi import WebSocket
from src.api.state import state
_last_status_payload: str | None = None

async def broadcast(data = None):
    '''向所有活跃 WebSocket 推送一条消息。

    一个慢连接（如 OBS 浏览器源跨网卡 / 网卡抖动）的 send_text 可能阻塞秒级，
    旧实现把所有 send 串在锁内 await，导致：
      - 全员都被这一个慢连接拖累，事件流卡顿
      - 锁被长期持有，其它代码加/删 ws 连接都被卡住
    现在改成：锁内只做 snapshot 取出连接集合，锁外用 gather 并行发送 + 收集死连接，
    最后再持锁清理死连接。
    '''
    pass
# WARNING: Decompyle incomplete


async def websocket_endpoint(websocket = None):
    pass
# WARNING: Decompyle incomplete


async def _ping_loop(websocket = None):
    pass
# WARNING: Decompyle incomplete

