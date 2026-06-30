from __future__ import annotations

import shutil
from pathlib import Path


def save_file_with_dialog(source_path: str | Path, default_name: str, _filters=None) -> str | None:
    source = Path(source_path)
    target = Path.cwd() / default_name
    try:
        shutil.copy2(source, target)
    except OSError:
        return None
    return str(target)
