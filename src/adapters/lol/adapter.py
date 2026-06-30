# Source Generated with Decompyle++
# File: adapter.pyc (Python 3.11)

'''LOL 适配器 — 组装 listener + mode，输出 DeviceCommand'''
import asyncio
import math
from src.adapters.triple_mode_adapter import TripleModeAdapter, ZeroHpDebouncer
from src.adapters.lol.listener import LOLListener
from src.adapters.lol.modes import NormalMode, FixedMode, ChallengeMode
from src.adapters.startup_check import startup_check, startup_step
from src.device.commands import DeviceCommand
from src.utils.logger import get_logger
logger = get_logger('LOL')
MODE_LABELS = {
    'normal': '动态强度',
    'fixed': '固定强度',
    'challenge': '挑战模式' }

class LOLAdapter(TripleModeAdapter):
    pass
# WARNING: Decompyle incomplete

