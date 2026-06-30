# Source Generated with Decompyle++
# File: adapter.pyc (Python 3.11)

'''CS2 适配器 — 组装 listener + mode，输出 DeviceCommand'''
import asyncio
import time
from src.adapters.triple_mode_adapter import TripleModeAdapter, ZeroHpDebouncer
from src.adapters.cs2.listener import CS2Listener
from src.adapters.cs2.modes import NormalMode, FixedMode, ChallengeMode
from src.adapters.cs2.custom_mode import CustomMode, CustomEventContext, RULE_NONE, RULE_LABELS
from src.adapters.startup_check import startup_check, startup_step
from src.utils.logger import get_logger
logger = get_logger('CS2')
MODE_LABELS = {
    'normal': '动态强度',
    'fixed': '固定强度',
    'challenge': '挑战模式',
    'custom': '自定义' }

class CS2Adapter(TripleModeAdapter):
    pass
# WARNING: Decompyle incomplete

