from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


PLUGIN_ROOT_ENV = "DGHUB_PLUGIN_ROOT"


def _path_key(path: str | os.PathLike[str]) -> str:
    return os.path.normcase(os.path.abspath(path))


def plugin_import_paths(
    script_path: str | os.PathLike[str],
    plugin_root: str | os.PathLike[str] | None = None,
) -> list[str]:
    """Return the import paths DGHub exposes to external Python plugins."""
    entry = Path(script_path).resolve()
    root_value = plugin_root or os.environ.get(PLUGIN_ROOT_ENV)
    root = Path(root_value).resolve() if root_value else entry.parent

    candidates = [
        entry.parent,
        root,
        entry.parent / "vendor",
        root / "vendor",
    ]

    paths: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate.is_dir():
            continue
        key = _path_key(candidate)
        if key in seen:
            continue
        seen.add(key)
        paths.append(str(candidate))
    return paths


def prepend_plugin_paths_to_sys_path(
    script_path: str | os.PathLike[str],
    plugin_root: str | os.PathLike[str] | None = None,
) -> list[str]:
    """Move plugin-local module paths to the front of sys.path."""
    paths = plugin_import_paths(script_path, plugin_root)
    for path in reversed(paths):
        key = _path_key(path)
        sys.path[:] = [item for item in sys.path if _path_key(item or ".") != key]
        sys.path.insert(0, path)
    return paths


def prepend_plugin_paths_to_env(
    env: dict[str, str],
    script_path: str | os.PathLike[str],
    plugin_root: str | os.PathLike[str] | None = None,
) -> None:
    """Prepare PYTHONPATH for plugin subprocesses."""
    paths = plugin_import_paths(script_path, plugin_root)
    paths.extend(item for item in env.get("PYTHONPATH", "").split(os.pathsep) if item)

    deduped: list[str] = []
    seen: set[str] = set()
    for path in paths:
        key = _path_key(path)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(path)

    env["PYTHONPATH"] = os.pathsep.join(deduped)
    if plugin_root:
        env[PLUGIN_ROOT_ENV] = str(Path(plugin_root).resolve())


def run_plugin_script(script_path: str | os.PathLike[str]) -> None:
    """Execute a plugin entry as __main__ and exit the runner process."""
    path = Path(script_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"插件 entry 不存在: {path}")
    prepend_plugin_paths_to_sys_path(path)
    sys.argv = [str(path)]
    runpy.run_path(str(path), run_name="__main__")
    sys.exit(0)
