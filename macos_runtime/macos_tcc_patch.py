from __future__ import annotations

import sys


BLUETOOTH_USAGE = "DGHub needs Bluetooth access to scan and connect DG-Lab devices."


def apply_tcc_usage_descriptions() -> None:
    if sys.platform != "darwin":
        return

    try:
        from Foundation import NSBundle
    except Exception:
        return

    try:
        info = NSBundle.mainBundle().infoDictionary()
        if info is None:
            return
        info["NSBluetoothAlwaysUsageDescription"] = BLUETOOTH_USAGE
        info["NSBluetoothPeripheralUsageDescription"] = BLUETOOTH_USAGE
    except Exception:
        return
