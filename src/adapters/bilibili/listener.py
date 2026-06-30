# Source Generated with Decompyle++
# File: listener.pyc (Python 3.11)

import asyncio
from bilibili_api import login_v2, live
import qrcode
import os
from src.utils.logger import get_logger
from src.utils import get_resource_path
logger = get_logger('Bilibili-Listener')

class BilibiliListener:
    
    def __init__(self, callback_danmaku, callback_gift, callback_sc, callback_guard = (None, None)):
        self.callback_danmaku = callback_danmaku
        self.callback_gift = callback_gift
        self.callback_sc = callback_sc
        self.callback_guard = callback_guard
        self.room = None
        self.is_running = False
        self.qrcode_path = ''
        self.login_status = '未登录'
        self.credential = None
        self.current_room_id = None
        self._task = None
        self._room_task = None

    
    async def start(self = None, room_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _run(self = None, room_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _login(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _connect_room(self = None, room_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def switch_room(self = None, room_id = None):
        '''切房间：断开当前 LiveDanmaku，用已有凭据连新的房间'''
        pass
    # WARNING: Decompyle incomplete

    
    async def _disconnect_room(self):
        pass
    # WARNING: Decompyle incomplete

    
    async def refresh_login(self):
        '''清除凭据并重新发起扫码登录（二维码过期时调用）。
        不停止 is_running，仅中断当前任务后重走 _login → _connect_room 流程。'''
        pass
    # WARNING: Decompyle incomplete

    
    async def stop(self):
        pass
    # WARNING: Decompyle incomplete


