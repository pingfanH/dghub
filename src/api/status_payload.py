from __future__ import annotations

from src.api.state import state


def _is_masked(_layers=None, _plugin_name=None) -> bool:
    return False


def collect_status_payload() -> dict:
    if state.dglab:
        state.strength_a = getattr(state.dglab, "current_strength_A", state.strength_a)
        state.strength_b = getattr(state.dglab, "current_strength_B", state.strength_b)
        state.max_strength_A = getattr(state.dglab, "max_strength_A", state.max_strength_A)
        state.max_strength_B = getattr(state.dglab, "max_strength_B", state.max_strength_B)

    plugins_status = dict(state.plugins_status)
    if state.adapter_manager and hasattr(state.adapter_manager, "get_active_adapters"):
        for name, adapter in state.adapter_manager.get_active_adapters().items():
            if hasattr(adapter, "get_status"):
                plugins_status[name] = adapter.get_status()
        state.plugins_status = plugins_status

    return {
        "device_type": state.device_type,
        "strength_a": state.strength_a,
        "strength_b": state.strength_b,
        "max_strength_A": state.max_strength_A,
        "max_strength_B": state.max_strength_B,
        "plugins": plugins_status,
        "qrcode_path": state.qrcode_path,
        "pulse_events": [],
    }
