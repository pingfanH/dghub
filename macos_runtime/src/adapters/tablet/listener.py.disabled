# Source Generated with Decompyle++
# File: listener.pyc (Python 3.11)

'''数位板 HID 压触轮询线程

笔尖压触状态从原始 HID 报文位 0 读取（与 pressure.py 一致）。
独立守护线程轮询，避免阻塞 asyncio 事件循环；通过回调把状态同步给适配器。
'''
import threading
import time
from src.utils.logger import get_logger
logger = get_logger('Tablet')

class TabletListener:
    
    def __init__(self = None, vid = None, on_drawing_change = None, on_pressure_tick = (None, None)):
        self.vid = vid
        self.on_drawing_change = on_drawing_change
        self.on_pressure_tick = on_pressure_tick
        self._thread = None
        self._stop_event = threading.Event()
        self.drawing = False
        self.device_connected = False
        self.last_error = ''
        self.device_count = 0

    
    def start(self):
        self._stop_event.clear()
        self._thread = threading.Thread(target = self._run, daemon = True, name = 'TabletHIDPoller')
        self._thread.start()

    
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout = 1)
            self._thread = None
            return None

    
    def _open_all(self):
        pass
    # WARNING: Decompyle incomplete

    
    def _run(self):
        handles = []
        retry_at = 0
    # WARNING: Decompyle incomplete


