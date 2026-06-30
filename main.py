from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RUNTIME_ROOT = ROOT
for candidate in (
    ROOT,
    ROOT / "macos_runtime",
):
    if (candidate / "main.pyc").exists():
        RUNTIME_ROOT = candidate
        break


def _link_or_copy_file(source: Path, target: Path) -> None:
    if target.exists() or not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.symlink_to(source)
    except OSError:
        shutil.copy2(source, target)


def _ensure_frontend_entrypoints() -> None:
    source_dist = ROOT / "src" / "frontend-vue" / "dist"
    runtime_roots = []
    if RUNTIME_ROOT != ROOT:
        runtime_roots.append(RUNTIME_ROOT)
    legacy_runtime = ROOT / "macos_runtime"
    if legacy_runtime.exists() and legacy_runtime not in runtime_roots:
        runtime_roots.append(legacy_runtime)

    for runtime_root in runtime_roots:
        for relative_dist in (
            Path("src/frontend-vue/dist"),
            Path("_internal/src/frontend-vue/dist"),
        ):
            target_dist = runtime_root / relative_dist
            for filename in ("index.html", "obs.html"):
                _link_or_copy_file(source_dist / filename, target_dist / filename)

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
    _ensure_frontend_entrypoints()

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
