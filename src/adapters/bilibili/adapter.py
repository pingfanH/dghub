# Source Generated with Decompyle++
# File: adapter.pyc (Python 3.11)

'''Bilibili 直播互动适配器 - layer-only 范式

核心模型：
- 闲置强度 (idle_strength): 插件当前的持久化锚点，事件回正时回到这里
- 运行时累积 (_persistent_pct): 弹幕投票等运行时叠加量，重启清零，不写盘
- baseline = clamp(idle_strength + _persistent_pct, 0, 100)
- 事件触发时实际强度 = min(100, baseline + 配置的 delta%)
- rollback 模式：layer 临时设到触发强度，duration 秒后回到 baseline
- permanent 模式：直接修改 idle_strength 配置，波形播完后回到新的锚点
'''
import asyncio
import functools
import math
import time
from collections import deque
from src.adapters.base import GameAdapter, pct_to_strength
from src.adapters.bilibili.config_mixin import BiliConfigMixin
from src.adapters.bilibili.events import EVENT_DEFS, FRAME_MS, GUARD_LEVEL_NAMES
from src.adapters.bilibili.handlers_mixin import BiliHandlersMixin
from src.adapters.bilibili.listener import BilibiliListener
from src.adapters.bilibili.spawn_mixin import BiliSpawnMixin
from src.adapters.mode_base import MAX_PULSE_DURATION_S
from src.device.commands import DeviceCommand
from src.utils.logger import get_logger
logger = get_logger('Bilibili')

class BilibiliAdapter(GameAdapter, BiliHandlersMixin, BiliSpawnMixin, BiliConfigMixin):
    pass
# WARNING: Decompyle incomplete

