# Source Generated with Decompyle++
# File: listener.pyc (Python 3.11)

'''CS2 GSI 监听器 — 只负责接收和解析 CS2 游戏状态数据'''
from aiohttp import web
from src.utils.logger import get_logger
logger = get_logger('CS2-Listener')

class CS2Listener:
    
    def __init__(self, callback):
        '''callback: async fn(event_type, data_dict) — 由 adapter 提供'''
        self.callback = callback
        self.app = web.Application()
        self.app.router.add_post('', self._handle_post)

    
    async def start(self, host, port = ('127.0.0.1', 3000)):
        pass
    # WARNING: Decompyle incomplete

    
    async def _handle_post(self, request):
        pass
    # WARNING: Decompyle incomplete

    
    async def stop(self):
        pass
    # WARNING: Decompyle incomplete


