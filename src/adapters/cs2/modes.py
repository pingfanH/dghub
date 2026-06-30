# Source Generated with Decompyle++
# File: modes.pyc (Python 3.11)

'''CS2 模式策略 — 在共享 Base*Mode 上只填 CS2 特有的公式与事件'''
from src.adapters.mode_base import BaseChallengeMode, BaseFixedMode, BaseNormalMode, ModeStrategy as _Base
from src.device.commands import DeviceCommand
CS2_DEFAULT_PULSE_MAP = {
    'hit': 'CS2-受伤',
    'flash': 'CS2-闪光',
    'smoke': 'CS2-烟雾',
    'burn': 'CS2-燃烧',
    'death': 'CS2-死亡' }

class ModeStrategy(_Base):
    pass
# WARNING: Decompyle incomplete


class NormalMode(ModeStrategy, BaseNormalMode):
    
    def dynamic_pct(self = None, health = None, **_):
        '''已损血量 × 转换率（hit）。'''
        hit = int(self.config.get_plugin(self.plugin_name, 'hit', 100))
        damage = max(0, min(100, 100 - max(0, int(health))))
        return max(0, min(100, int(damage * hit / 100)))

    
    def dynamic_pct_for_health(self = None, health = None):
        '''按当前血量估算动态层目标，用于切模式时一次性对齐。'''
        return self.dynamic_pct(health = health)

    
    def baseline_cmds(self = None, health = None):
        '''切到动态模式：按当前血量一次性 set 到目标（含满血清残留），不先归零再等受伤。'''
        return self.dynamic_baseline_cmds(health = health)

    
    def on_death(self = None, health_before = None):
        return self.dynamic_death_cmds({
            'health': health_before }, {
            'health': 0 })



class FixedMode(ModeStrategy, BaseFixedMode):
    HURT_EVENT = 'hit'
    
    def on_flash(self = None):
        return self.fixed_event_cmds('flash')

    
    def on_smoke(self = None):
        return self.fixed_event_cmds('smoke')

    
    def on_burn(self = None):
        return self.fixed_event_cmds('burn')



class ChallengeMode(ModeStrategy, BaseChallengeMode):
    HURT_EVENT = 'hit'
    
    def on_flash(self = None):
        return self.challenge_event_cmds('flash')

    
    def on_smoke(self = None):
        return self.challenge_event_cmds('smoke')

    
    def on_burn(self = None):
        return self.challenge_event_cmds('burn')


