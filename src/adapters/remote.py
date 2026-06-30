# Source Generated with Decompyle++
# File: remote.pyc (Python 3.11)

'''远程插件运行时 — 把 WebSocket 连接桥接成普通 GameAdapter。

放在同一文件是为了让 ``RemoteAdapter`` 和 ``PluginRuntime`` 自由互引用，
不需要单独抽 protocol 层。

设计：
- 每个连接的远程插件 = 一个 ``RemoteAdapter`` + 一个 ``PluginRuntime``
- ``RemoteAdapter`` 被 ``AdapterManager._active`` 持有，对外表现跟内置插件 100% 一致
  （继承自 GameAdapter，复用所有强度 / 波形 helper）
- ``PluginRuntime`` 持有 WebSocket，跑收发循环，把消息分发给 adapter 状态机

WebSocket 消息处理是 best-effort：单条消息解析失败只 log，不杀连接；
但 ``hello`` 之外的协议错误也不影响别的插件，整个运行时是隔离的。
'''
from __future__ import annotations
import asyncio
import time
from typing import Any, TYPE_CHECKING
from fastapi import WebSocket
from pydantic import TypeAdapter, ValidationError
from src.adapters.base import GameAdapter, pct_to_strength
from src.adapters.startup_check import manifest_supports_startup_check, sanitize_startup_check
from src.adapters.sdk.protocol import SDK_MAJOR, ClientMsg, HelloMsg, EventMsg, PulseMsg, SetStrengthMsg, AdjustStrengthMsg, TriggerMsg, StatusMsg, LogMsg, SetConfigMsg, HelloAckMsg, ConfigMsg, ConfigChangedMsg, DeviceInfoMsg, StopMsg, PluginManifest
from src.utils.logger import get_logger
if TYPE_CHECKING:
    from src.adapters.sdk.protocol import ServerMsg
DEFAULT_EVENT_DURATION_S = 1
_client_msg_adapter = TypeAdapter(ClientMsg)

class RemoteAdapter(GameAdapter):
    pass
# WARNING: Decompyle incomplete


class PluginRuntime:
    '''单个远程插件的 WebSocket 收发循环 + 消息分发。

    生命周期：``run()`` 抛出 / 返回 = 该插件下线，调用方负责 cleanup。
    '''
    
    def __init__(self = None, websocket = None, adapter = None, *, manager, config_manager, on_disconnect):
        self.ws = websocket
        self.adapter = adapter
        self.manager = manager
        self.config = config_manager
        self.on_disconnect = on_disconnect
        self.logger = get_logger(f'''Plugin[{adapter.plugin_name}]''')
        self._closed = False
        self._send_lock = asyncio.Lock()

    plugin_id = (lambda self = None: self.adapter.plugin_name)()
    
    async def run(self = None):
        '''阻塞跑直到连接断开。'''
        pass
    # WARNING: Decompyle incomplete

    
    async def shutdown(self = None, reason = None):
        '''主程序主动断开 — 发 StopMsg 后关闭。'''
        pass
    # WARNING: Decompyle incomplete

    
    async def push_config_changed(self = None, key = None, value = None):
        '''前端 / 主程序改了配置后通知插件。'''
        pass
    # WARNING: Decompyle incomplete

    
    async def push_device_info(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _push_initial_state(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _send(self = None, msg = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _close_ws(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _handle_raw(self = None, raw = None):
        pass
    # WARNING: Decompyle incomplete

    
    async def _dispatch(self = None, msg = None):
        pass
    # WARNING: Decompyle incomplete



def make_hello_ack(*, accepted, reason):
    return HelloAckMsg(op = 'hello_ack', accepted = accepted, reason = reason)


def check_sdk_compat(sdk_field = None):
    '''检查插件 manifest.sdk 跟主程序 SDK_MAJOR 是否兼容。

    Returns: (ok, reason_if_failed)
    '''
    
    try:
        major = int(str(sdk_field).split('.')[0])
    except (ValueError, IndexError):
        return 

    if major != SDK_MAJOR:
        return (False, f'''SDK 主版本不匹配：插件需要 {major}.x，本程序为 {SDK_MAJOR}.x''')

