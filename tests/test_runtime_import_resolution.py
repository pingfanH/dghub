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
import src.overlay.desktop_overlay as overlay

get_logger("ImportTest")
print(Path(overlay.__file__).resolve())
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
            Path(result.stdout.strip()),
            ROOT / "src" / "overlay" / "desktop_overlay.py",
        )


if __name__ == "__main__":
    unittest.main()
