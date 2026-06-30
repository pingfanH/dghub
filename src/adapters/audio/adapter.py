# Source Generated with Decompyle++
# File: adapter.pyc (Python 3.11)

import asyncio
import numpy as np
from src.adapters.base import GameAdapter
from src.adapters.runtime_sync import schedule_async
from src.utils.audio_kit import BASE_GAIN
from src.utils.logger import get_logger
AUDIO_SYNC_KEYS = frozenset({
    'channel',
    'threshold',
    'sensitivity',
    'audio_action'})
logger = get_logger('Audio')
ACTION_LABELS = {
    'pulse': '脉冲',
    'adjust': '强度调节',
    'both': '强度+脉冲' }

class AudioAdapter(GameAdapter):
    pass
# WARNING: Decompyle incomplete

