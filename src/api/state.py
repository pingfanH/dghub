# Source Generated with Decompyle++
# File: state.pyc (Python 3.11)

'''全局应用状态'''
import asyncio
import secrets

class AppState:
    
    def __init__(self):
        self.dglab = None
        self.adapter_manager = None
        self.websocket_connections = set()
        self._ws_lock = asyncio.Lock()
        self.strength_a = 0
        self.strength_b = 0
        self.max_strength_A = 0
        self.max_strength_B = 0
        self.plugins_status = { }
        self.qrcode_path = ''
        self.device_type = 'v3'
        self._monitor_task = None
        self.plugin_session_token = secrets.token_urlsafe(32)


state = AppState()
