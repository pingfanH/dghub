# Source Generated with Decompyle++
# File: status_payload.pyc (Python 3.11)

'''状态广播 payload 收集 — 从 api/app.py 拆出。

把设备强度、各插件 get_status、强度层 masked 标记、波形事件
汇总成 WebSocket `status_update` 消息体。monitor 循环按需调用。
'''
from src.api.state import state

def _is_masked(layers = None, plugin_name = None):
    '''计算插件当前是否被其它插件的强度层 "盖掉"（masked）。

    规则：插件在某个通道领先（自己非零且严格大于其它所有插件） → not masked；
    反之插件在所有非零通道都被压制，则视为 masked。供 OBS 卡片显示「⛓ 被覆盖」。
    '''
    pass
# WARNING: Decompyle incomplete


def collect_status_payload():
    '''采集当前完整状态快照；设备未就绪时返回 None。

    有副作用：把设备实时强度回写到 state.strength_* / state.plugins_status。
    '''
    if not state.dglab:
        return None
    state.strength_a = None.dglab.current_strength_A
    state.strength_b = state.dglab.current_strength_B
    state.max_strength_A = state.dglab.max_strength_A
    state.max_strength_B = state.dglab.max_strength_B
    plugins_status = { }
    if state.adapter_manager:
        for name, adapter in state.adapter_manager.get_active_adapters().items():
            if hasattr(adapter, 'get_status'):
                plugins_status[name] = adapter.get_status()
            state.plugins_status = plugins_status
    layers = state.dglab.strength_layers.get_layers() if state.dglab and state.dglab.strength_layers else { }
    pulse_events = []
# WARNING: Decompyle incomplete

