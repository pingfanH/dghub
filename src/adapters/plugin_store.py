from __future__ import annotations

from pathlib import Path


def get_plugins_dir() -> Path:
    path = Path.cwd() / "plugins"
    path.mkdir(exist_ok=True)
    return path
