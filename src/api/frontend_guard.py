from __future__ import annotations

from pathlib import Path

from fastapi.responses import HTMLResponse


REQUIRED_FRONTEND_FILES = ("index.html",)


def _frontend_candidates() -> list[Path]:
    root = Path.cwd()
    return [
        root / "src/frontend-vue/dist",
        root / "macos_runtime/src/frontend-vue/dist",
        root / "macos_runtime/_internal/src/frontend-vue/dist",
    ]


def _find_frontend_path() -> Path | None:
    for candidate in _frontend_candidates():
        if (candidate / "index.html").exists():
            return candidate
    return None


def _check_frontend_integrity(frontend_path: Path) -> list[str]:
    return [name for name in REQUIRED_FRONTEND_FILES if not (frontend_path / name).exists()]


def _serve_index_or_diagnostic() -> HTMLResponse:
    frontend = _find_frontend_path()
    if frontend and not _check_frontend_integrity(frontend):
        return HTMLResponse((frontend / "index.html").read_text(encoding="utf-8"))
    checked = "\n".join(f"<li>{path}</li>" for path in _frontend_candidates())
    return HTMLResponse(
        f"<h1>DGHub 前端资源缺失</h1><p>没有找到 src/frontend-vue/dist/index.html。</p><ul>{checked}</ul>",
        status_code=503,
    )
