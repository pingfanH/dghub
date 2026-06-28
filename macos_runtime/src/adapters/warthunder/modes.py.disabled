# Source Generated with Decompyle++
# File: modes.pyc (Python 3.11)

'''War Thunder 模式策略 — 每个事件可独立 override 强度行为

设计哲学（与 Bilibili 插件对齐）：
- 顶层"模式"（normal/fixed/challenge）只是"批量给所有事件的强度行为填默认值"
- 每个事件可以单独 override 自己的强度行为（strength_action_<event>）
- 波形（pulse_<event>）与持续时长（duration_<event>）始终由事件配置决定，与模式无关

per-event override 机制（follow/none/increase/decrease/set + ``on_event`` 统一入口）
已上收到 :mod:`src.adapters.mode_base`，这里只剩 WT 特有的模式默认行为。
旧 on_hurt/on_death/... hook 保留作 thin wrapper 以避免 adapter 大改。
'''
from src.adapters.base import pct_to_strength
from src.adapters.mode_base import BaseChallengeMode, BaseFixedMode, ModeStrategy as _Base
from src.device.commands import DeviceCommand
WT_DEFAULT_PULSE_MAP = {
    'hit': 'CS2-受伤',
    'death': 'CS2-死亡',
    'kill': 'CS2-受伤',
    'crash': 'CS2-死亡',
    'fire': 'CS2-燃烧',
    'crew_lost': 'CS2-受伤',
    'track_broken': 'CS2-受伤',
    'high_g': 'CS2-受伤' }

class ModeStrategy(_Base):
    pass
# WARNING: Decompyle incomplete


class NormalMode(ModeStrategy):
    '''动态模式 — 默认行为：受伤按伤害比例累加强度，其他事件仅播波形。

    设计意图：动态模式特点是用伤害驱动强度爬升（"打得越惨越上头"），其他事件不打断这条曲线。
    用户为非 hit 事件配置 strength_action 时可以单独 override（例如让"击杀"额外 +20%）。
    '''
    
    def _default_strength_cmds(self, event_name, channel, dmg_pct = (None,)):
        pass
    # WARNING: Decompyle incomplete



class FixedMode(ModeStrategy, BaseFixedMode):
    '''固定模式 — 默认所有事件触发时都把强度设到 fixed_mode_strength。'''
    on_hurt = ModeStrategy.on_hurt
    
    def _default_strength_cmds(self, event_name, channel, dmg_pct = (None,)):
        return self._set_fixed_strength(channel = channel)



class ChallengeMode(ModeStrategy, BaseChallengeMode):
    '''挑战模式 — 维护 current_strength 状态变量：

    - 击杀 → current -= reduction
    - 死亡 / 坠毁 → current += boost
    - 其他事件 → 维持 current（重新 set 一遍，刷新 strength layer）
    '''
    on_hurt = ModeStrategy.on_hurt
    on_kill = ModeStrategy.on_kill
    on_death = ModeStrategy.on_death
    
    def _default_strength_cmds(self, event_name, channel, dmg_pct = (None,)):
        if event_name == 'kill':
            self.apply_kill_reduction()
        elif event_name in ('death', 'crash'):
            self.apply_death_boost()
        return self._strength_set_pct(self.current_strength, channel = channel)


