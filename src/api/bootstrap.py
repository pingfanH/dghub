# Source Generated with Decompyle++
# File: bootstrap.pyc (Python 3.11)

'''启动编排 — 从 api/app.py 拆出。

start_background_tasks 按职责拆为独立步骤：
设备初始化（_init_device）→ 插件管理器与恢复（_init_adapter_manager / _restore_enabled_plugins）
→ 状态监控广播（_start_monitor）。
switch_device_type 复用同一套设备创建逻辑。
'''
import asyncio
import copy
import os
from src.api.deps import get_config, get_preset_mgr
from src.api.state import state
from src.api.status_payload import collect_status_payload
from src.api.websocket import broadcast
from src.device.controller import DGLabV3Controller
from src.utils import get_resource_path, get_local_ip, generate_qrcode
from src.utils.logger import get_logger, memory_handler
logger = get_logger('System')

def _create_v2_controller(config):
    DGLabV2Controller = DGLabV2Controller
    import src.device.v2_controller
    return DGLabV2Controller(config = config)


async def _create_v3_controller():
    '''创建 V3 控制器、等待客户端就绪并生成二维码。返回 (controller, qrcode_path)。'''
    pass
# WARNING: Decompyle incomplete


async def _init_device(config):
    '''按配置创建设备控制器并写入 state。'''
    pass
# WARNING: Decompyle incomplete


def _init_adapter_manager(config, preset_manager):
    '''创建插件管理器、扫描外部插件、注入远程接入参数。'''
    AdapterManager = AdapterManager
    import src.adapters.manager
    state.adapter_manager = AdapterManager(config, state.dglab.queue, state.dglab.get_device_info, preset_manager, state.dglab.strength_layers)
    state.adapter_manager.discover_installed_plugins()
    server_port = int(os.environ.get('DGHUB_SERVER_PORT', '0'))
    state.adapter_manager.configure_remote(host = '127.0.0.1', port = server_port, token = state.plugin_session_token)


async def _restore_enabled_plugins(config):
    '''按 config 恢复上次启用的插件（不改写 enabled；单个失败不拖垮启动）。'''
    pass
# WARNING: Decompyle incomplete

_MONITOR_FALLBACK_SEC = 1

def _start_monitor():
    '''启动状态监控（delta-based，有变化才广播）并挂接日志推送。'''
    pass
# WARNING: Decompyle incomplete


async def start_background_tasks():
    pass
# WARNING: Decompyle incomplete


async def switch_device_type(new_type = None):
    '''运行时切换设备类型：停止插件 → 停旧控制器 → 创建新控制器 → 重绑插件引用'''
    pass
# WARNING: Decompyle incomplete

