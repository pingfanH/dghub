# Source Generated with Decompyle++
# File: listener.pyc (Python 3.11)

'''MC Listener — 连接 DGHub-MC Mod 的 WebSocket Server，接收游戏事件并推送设备状态'''
import asyncio
import json
import aiohttp
from src.utils.logger import get_logger
logger = get_logger('MC-Listener')

class MCListener:
    
    def __init__(self, callback, status_provider):
        '''
        callback: async fn(data: dict) — 接收解析后的游戏事件
        status_provider: callable returning dict with device strength/connection info
        '''
        self.callback = callback
        self.status_provider = status_provider
        self._running = False
        self._task = None
        self._status_task = None
        self._connected = False
        self._ws = None

    is_connected = (lambda self = None: self._connected)()
    
    async def start(self, host, port = ('127.0.0.1', 9999)):
        pass
    # WARNING: Decompyle incomplete

    
    async def _connect_loop(self):
        pass
    # WARNING: Decompyle incomplete

    
    async def _handle_session(self, ws):
        pass
    # WARNING: Decompyle incomplete

    
    async def _push_status_loop(self, ws):
        '''定期向 Mod 推送设备状态用于 HUD 显示

        ws 关闭/异常时自然退出（外层会重连）；
        瞬时发送失败不退出循环 — 之前的 break 会导致 HUD 在 ws 还活着时永久卡住。
        '''
        pass
    # WARNING: Decompyle incomplete

    
    async def send_action(self = None, payload = None):
        '''向已连接的 MC mod 发送一条 action 消息（如召唤怪物）。

        Mod 未连接或 ws 已关闭时静默 drop 并返回 False，不抛异常。
        '''
        pass
    # WARNING: Decompyle incomplete

    
    async def stop(self):
        pass
    # WARNING: Decompyle incomplete


