# Source Generated with Decompyle++
# File: adapter.pyc (Python 3.11)

import asyncio
import time
import threading
from collections import deque
from src.adapters.base import GameAdapter
from src.adapters.startup_check import startup_check, startup_step
from src.device.commands import DeviceCommand
from src.utils.logger import get_logger
logger = get_logger('VRChat')
CONDITION_FNS = {
    'equal': (lambda v, t: v == t),
    'greater': (lambda v, t: v > t),
    'less': (lambda v, t: v < t),
    'not_equal': (lambda v, t: v != t) }
CONDITION_LABELS = {
    'equal': '==',
    'greater': '>',
    'less': '<',
    'not_equal': '!=',
    'change': '变化' }
ACTION_LABELS = {
    'pulse': '脉冲',
    'adjust': '强度调节',
    'both': '强度+脉冲' }
MAX_RECENT_PARAMS = 50
CHATBOX_MIN_INTERVAL = 2

class VRChatAdapter(GameAdapter):
    pass
# WARNING: Decompyle incomplete

