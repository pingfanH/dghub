# Source Generated with Decompyle++
# File: adapter.pyc (Python 3.11)

'''数位板（数控版外设）适配器

行为：当数位板检测到笔尖在 idle_threshold 秒内没有压触动作时，按配置下发强度层和/或波形。
冷却 = 0：单次触发，等用户再画一笔后才能再触发。
冷却 > 0：触发后若仍处于闲置状态，每 cooldown 秒重复触发。
'''
import asyncio
import math
import time
from src.adapters.base import GameAdapter
from src.adapters.tablet.listener import TabletListener
from src.device.commands import DeviceCommand
from src.utils.logger import get_logger
logger = get_logger('Tablet')
DEFAULT_VID = 9580
FRAME_MS = 100
MAX_PULSE_DURATION_S = 30
ACTION_LABELS = {
    'pulse': '脉冲',
    'adjust': '强度调节',
    'both': '强度+脉冲' }

class TabletAdapter(GameAdapter):
    pass
# WARNING: Decompyle incomplete

