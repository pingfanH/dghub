# Source Generated with Decompyle++
# File: modes.pyc (Python 3.11)

'''LOL 模式策略 — 在共享 Base*Mode 上只填 LOL 特有的公式与事件'''
from src.adapters.mode_base import BaseChallengeMode, BaseFixedMode, BaseNormalMode, ModeStrategy as _Base
from src.device.commands import DeviceCommand
LOL_DEFAULT_PULSE_MAP = {
    'hurt': 'CS2-受伤',
    'death': 'CS2-死亡',
    'kill': 'CS2-受伤' }

class ModeStrategy(_Base):
    pass
# WARNING: Decompyle incomplete


class NormalMode(ModeStrategy, BaseNormalMode):
    '''动态模式 — 强度随当前血量百分比变化，血越低强度越高'''
    
    def dynamic_pct(self = None, hp_percent = None, **_):
        base_pct = int(self.config.get_plugin(self.plugin_name, 'dynamic_base', 80))
        return max(0, min(100, int((1 - hp_percent / 100) * base_pct)))

    
    def baseline_cmds(self = None, hp_percent = None):
        return self.dynamic_baseline_cmds(hp_percent = hp_percent)

    
    def on_health_update(self = None, hp_percent = None):
        return self.dynamic_baseline_cmds(hp_percent = hp_percent)

    
    def on_hurt(self = None, hp_percent = None):
        return self.dynamic_baseline_cmds(hp_percent = hp_percent) + [
            self.make_pulse('hurt')]

    
    def on_death(self = None):
        base_pct = int(self.config.get_plugin(self.plugin_name, 'dynamic_base', 80))
        return self._strength_set_pct(base_pct) + [
            self.make_pulse('death')]



class FixedMode(ModeStrategy, BaseFixedMode):
    '''固定模式 — 所有事件使用固定强度（强度走插件全局通道，旧行为）'''
    HURT_EVENT = 'hurt'
    STRENGTH_ON_EVENT_CHANNEL = False


class ChallengeMode(ModeStrategy, BaseChallengeMode):
    '''挑战模式 — 击杀降低强度，死亡增加强度'''
    HURT_EVENT = 'hurt'
    STRENGTH_ON_EVENT_CHANNEL = False

