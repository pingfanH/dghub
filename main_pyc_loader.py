from __future__ import annotations

import marshal
from pathlib import Path
from types import CodeType


def load_main_pyc() -> dict:
    root = Path(__file__).resolve().parent
    candidates = (
        root / "main.pyc",
        root / "macos_runtime" / "main.pyc",
    )
    path = next((candidate for candidate in candidates if candidate.exists()), candidates[0])
    code = marshal.loads(path.read_bytes()[16:])
    module_globals = {
        "__name__": "dghub_original_main",
        "__file__": str(path),
        "__package__": "",
    }
    exec(code, module_globals)
    return module_globals
