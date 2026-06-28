# Source Generated with Decompyle++
# File: bili_mc_routes.pyc (Python 3.11)

__doc__ = 'B站 → MC 召怪扩展功能 — 加密配置面板路由\n\n设计：前端 SHA-256 hash 密码 → 后端比对硬编码 hash → 发 uuid token；\n后续读写召怪配置的请求必须带 token，token 仅存内存（进程重启即失效，符合"会话级"语义）。\n\n注意：此 token 仅用于 UI 配置面板，不参与 B站 → MC 召怪触发链路（那是后端内部链路）。\n'
import hashlib
import time
import uuid
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from src.api.deps import get_config
from src.utils.logger import get_logger
logger = get_logger('BiliMC-Routes')
router = APIRouter(prefix = '/api/bili-mc')
_PWD_HASH = hashlib.sha256(b'1879857116').hexdigest()
_unlocked_tokens: dict[(str, float)] = { }
_TOKEN_TTL_SEC = 3600
_MAX_UNLOCK_ATTEMPTS = 8
_UNLOCK_WINDOW_SEC = 60
_unlock_fail_times: list[float] = []

def _prune_tokens():
    pass
# WARNING: Decompyle incomplete


def _register_token(token = None):
    _prune_tokens()
    _unlocked_tokens[token] = time.monotonic() + _TOKEN_TTL_SEC


def _consume_unlock_attempt():
    '''返回 True 表示仍允许尝试解锁。'''
    pass
# WARNING: Decompyle incomplete

_ALLOWED_CONFIG_KEYS = {
    'spawn_radius_max',
    'spawn_radius_min',
    'spawn_cap_in_radius',
    'spawn_max_per_event',
    'event_sc_spawn_rules',
    'event_gift_spawn_rules',
    'event_sc_spawn_enabled',
    'event_guard_spawn_rules',
    'event_gift_spawn_enabled',
    'event_danmaku_spawn_rules',
    'event_guard_spawn_enabled',
    'event_sc_spawn_default_mob',
    'event_danmaku_spawn_enabled',
    'event_gift_spawn_default_mob',
    'event_guard_spawn_default_mob',
    'event_danmaku_spawn_default_mob'}
# WARNING: Decompyle incomplete
