from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RuntimeImportResolutionTest(unittest.TestCase):
    def test_runtime_dependencies_and_overlay_source_override_can_coexist(self) -> None:
        code = """
import main
from pathlib import Path
from src.utils.logger import get_logger
import src.api.overlay_manager as overlay_manager
import src.overlay.desktop_overlay as overlay

get_logger("ImportTest")
manager = overlay_manager.OverlayManager()
manager._token = "token"
argv = manager._build_argv(8123, overlay_manager.normalize_config({}))
print(Path(overlay_manager.__file__).resolve())
print(Path(overlay.__file__).resolve())
print(Path(argv[1]).resolve())
"""
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                str(ROOT / "src" / "api" / "overlay_manager.py"),
                str(ROOT / "src" / "overlay" / "desktop_overlay.py"),
                str(ROOT / "main.py"),
            ],
        )

    def test_overlay_manager_starts_overlay_through_root_main(self) -> None:
        code = """
import main
from pathlib import Path
import src.api.overlay_manager as overlay_manager

captured = {}

class FakeProc:
    pid = 4242

    def __init__(self):
        self.returncode = None

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        self.returncode = 0

def fake_spawn(argv, **kwargs):
    captured["argv"] = argv
    captured["cwd"] = kwargs.get("cwd")
    captured["stdout"] = Path(kwargs["stdout"].name).name
    return FakeProc()

overlay_manager.spawn_managed_subprocess = fake_spawn
overlay_manager.OVERLAY_LOG = Path("logs/test-overlay-subprocess.log")

manager = overlay_manager.OverlayManager()
ok = manager.start(8123, {})

print(ok)
print(manager.is_running())
print(Path(captured["argv"][1]).resolve())
print(captured["argv"][2])
print("--locked" in captured["argv"])
print(Path(captured["cwd"]).name)
print(captured["stdout"])
"""
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "True",
                "True",
                str(ROOT / "main.py"),
                "--overlay",
                "True",
                "macos_runtime",
                "test-overlay-subprocess.log",
            ],
        )


if __name__ == "__main__":
    unittest.main()
