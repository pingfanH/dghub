from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RUNTIME_ROOT = ROOT
if not (RUNTIME_ROOT / "main.pyc").exists() and (ROOT / "macos_runtime" / "main.pyc").exists():
    RUNTIME_ROOT = ROOT / "macos_runtime"

os.chdir(RUNTIME_ROOT)
sys.argv[0] = str(RUNTIME_ROOT / "main.py")
for path in (RUNTIME_ROOT, ROOT):
    path_text = str(path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)


def main() -> None:
    import multiprocessing

    multiprocessing.freeze_support()

    from macos_tcc_patch import apply_tcc_usage_descriptions

    apply_tcc_usage_descriptions()

    from src.utils.logger import get_logger

    log = get_logger("Boot")
    log.info(f"=== DGHub macOS runtime starting === argv={sys.argv}")

    from pydglab_macos_patch import apply_patches

    apply_patches()

    from src.api.app import _check_frontend_integrity, _find_frontend_path

    frontend = _find_frontend_path()
    if frontend:
        missing = _check_frontend_integrity(frontend)
        if missing:
            log.warning(f"frontend integrity warning path={frontend} missing={missing[:5]}")
        else:
            log.info(f"frontend OK path={frontend}")
    else:
        log.warning("frontend dist NOT FOUND")

    from main_pyc_loader import load_main_pyc

    original_main = load_main_pyc()

    if "--server" in sys.argv:
        original_main["start_server"]()
        return

    if "--overlay" in sys.argv:
        original_main["_maybe_run_overlay"]()
        return

    if "--plugin-runner" in sys.argv:
        original_main["_maybe_run_plugin_runner"]()
        return

    original_main["start_desktop_app"]()


if __name__ == "__main__":
    main()
