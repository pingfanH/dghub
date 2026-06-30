# Source Generated with Decompyle++
# File: adapter.pyc (Python 3.11)

'''Minimal Douyin live adapter.'''
from __future__ import annotations
import asyncio
import os
from pathlib import Path
import time
from src.adapters.base import GameAdapter
from src.adapters.douyin.events import EVENT_DEFS
from src.adapters.douyin.listener import DEFAULT_SOURCE, DouyinListener, DouyinListenerError
from src.adapters.douyin.normalizer import DouyinEvent, LikeAggregator, normalize_douyin_event
from src.utils.logger import get_logger
logger = get_logger('Douyin')

class DouyinAdapter(GameAdapter):
    pass
# WARNING: Decompyle incomplete

