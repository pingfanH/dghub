# Source Generated with Decompyle++
# File: modes.pyc (Python 3.11)

'''MC 模式策略 — 在共享 Base*Mode 上只填 MC 特有的公式与事件'''
from src.adapters.mode_base import BaseChallengeMode, BaseFixedMode, BaseNormalMode, ModeStrategy as _Base
from src.device.commands import DeviceCommand
MC_DEFAULT_PULSE_MAP = {
    'hurt': 'CS2-受伤',
    'death': 'CS2-死亡' }

class ModeStrategy(_Base):
    pass
# WARNING: Decompyle incomplete


class NormalMode(ModeStrategy, BaseNormalMode):
    '''动态模式 — 根据血量缺失比例实时设置强度（满血=0，空血=最大强度×转换率）'''
    
    def dynamic_pct(self = None, health = None, max_health = None, **_):
        ratio = int(self.config.get_plugin(self.plugin_name, 'damage_ratio', 100))
        if max_health <= 0:
            max_health = 20
        lost_pct = max(0, min(1, 1 - health / max_health))
        return int(lost_pct * ratio)

    
    def baseline_cmds(self = None, health = None, max_health = None):
        return self.dynamic_baseline_cmds(health = health, max_health = max_health)

    
    def on_health_update(self = None, health = None, max_health = None):
        return self.dynamic_baseline_cmds(health = health, max_health = max_health)

    
    def on_hurt(self = None, _damage_value = None, health = None, max_health = (0, 20)):
        return self.dynamic_baseline_cmds(health = health, max_health = max_health) + [
            self.make_pulse('hurt')]

    
    def on_death(self = None, health_before = None, max_health = None):
        return self.dynamic_death_cmds({
            'health': health_before,
            'max_health': max_health }, {
            'health': 0,
            'max_health': max_health })



class FixedMode(ModeStrategy, BaseFixedMode):
    '''固定模式 — 所有事件使用固定强度（强度走插件全局通道，旧行为）'''
    HURT_EVENT = 'hurt'
    STRENGTH_ON_EVENT_CHANNEL = False


class ChallengeMode(ModeStrategy, BaseChallengeMode):
    '''挑战模式 — 死亡增加强度（MC 没有击杀事件，所以只做死亡加强）'''
    HURT_EVENT = 'hurt'
    STRENGTH_ON_EVENT_CHANNEL = False

