# Source Generated with Decompyle++
# File: triple_mode_adapter.pyc (Python 3.11)

'''三模式游戏适配器中间基类 — CS2 / LOL / MC / 战雷共用的模式生命周期与事件流基建。

吸收 4 个游戏 adapter 各自重复的 ~150 行样板：
- 模式生命周期：``MODE_CLASS_MAP`` + ``_create_mode/refresh_mode/_ensure_mode_synced``
  （含 ``_applied_config_mode`` 配置切换比对）
- baseline：``_mode_baseline_cmds/_sync_mode_baseline/_mode_baseline_pct``
  （动态模式上下文由 :meth:`_normal_baseline_ctx` 钩子提供）
- 事件流：``_event_pulse_for/_event_duration``（``_push_event``/``_recent_events`` 在 GameAdapter）
- ``ZeroHpDebouncer``：连续 HP=0 帧去抖（CS2 GSI / LOL LCU 同源思路）
'''
from src.adapters.base import GameAdapter
from src.adapters.mode_base import BaseChallengeMode, BaseFixedMode, BaseNormalMode
from src.adapters.runtime_sync import TRIPLE_MODE_SYNC_KEYS, read_config_mode
DEFAULT_MODE_LABELS = {
    'normal': '动态强度',
    'fixed': '固定强度',
    'challenge': '挑战模式' }

class ZeroHpDebouncer:
    '''连续 HP=0 帧计数 — 过滤数据源单帧抖动产生的假死亡 / 假复活。'''
    
    def __init__(self = None, confirm_frames = None):
        self.confirm_frames = confirm_frames
        self.streak = 0

    
    def push_zero(self = None):
        '''本帧 HP=0 → 计数 +1，返回当前连续帧数。'''
        return self.streak

    confirmed = (lambda self = None: self.streak >= self.confirm_frames)()
    
    def reset(self = None):
        self.streak = 0



class TripleModeAdapter(GameAdapter):
    pass
# WARNING: Decompyle incomplete

