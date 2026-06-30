from __future__ import annotations

import sys
import plistlib
from pathlib import Path


BLUETOOTH_USAGE = "DGHub needs Bluetooth access to scan and connect DG-Lab devices."


def apply_tcc_usage_descriptions() -> None:
    if sys.platform != "darwin":
        return

    _patch_python_app_info_plist()

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


def _patch_python_app_info_plist() -> None:
    plist_path = _python_app_info_plist()
    if plist_path is None or not plist_path.is_file():
        return

    try:
        data = plistlib.loads(plist_path.read_bytes())
        changed = False
        for key in ("NSBluetoothAlwaysUsageDescription", "NSBluetoothPeripheralUsageDescription"):
            if data.get(key) != BLUETOOTH_USAGE:
                data[key] = BLUETOOTH_USAGE
                changed = True
        if changed:
            plist_path.write_bytes(plistlib.dumps(data, sort_keys=False))
    except Exception:
        return


def _python_app_info_plist() -> Path | None:
    candidates: list[Path] = []

    for value in (getattr(sys, "base_prefix", ""), getattr(sys, "prefix", "")):
        if value:
            candidates.append(Path(value))

    executable = Path(sys.executable).resolve()
    candidates.extend(executable.parents)

    for base in candidates:
        plist_path = base / "Resources" / "Python.app" / "Contents" / "Info.plist"
        if plist_path.is_file():
            return plist_path
    return None
