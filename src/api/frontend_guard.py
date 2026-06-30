from __future__ import annotations

import re
from pathlib import Path

from fastapi.responses import HTMLResponse


STATIC_REF_RE = re.compile(r'''(?:src|href)=["'](?:/static/)?([^"']+)["']''')


def _frontend_candidates() -> list[Path]:
    root = Path.cwd()
    return [
        root / "macos_runtime/src/frontend-vue/dist",
        root / "macos_runtime/_internal/src/frontend-vue/dist",
        root / "src/frontend-vue/dist",
    ]


def _find_frontend_path() -> Path | None:
    fallback = None
    for candidate in _frontend_candidates():
        if not (candidate / "index.html").exists():
            continue
        if fallback is None:
            fallback = candidate
        if not _check_frontend_integrity(candidate):
            return candidate
    return fallback


def _check_frontend_integrity(frontend_path: Path) -> list[str]:
    index = frontend_path / "index.html"
    if not index.exists():
        return ["index.html"]
    missing = []
    html = index.read_text(encoding="utf-8", errors="ignore")
    for ref in STATIC_REF_RE.findall(html):
        if ref.startswith(("http://", "https://", "data:")):
            continue
        relative = ref.lstrip("/")
        if not (frontend_path / relative).exists():
            missing.append(relative)
    return missing


def _serve_index_or_diagnostic() -> HTMLResponse:
    frontend = _find_frontend_path()
    if frontend and not _check_frontend_integrity(frontend):
        return HTMLResponse((frontend / "index.html").read_text(encoding="utf-8"))
    checked = "\n".join(f"<li>{path}</li>" for path in _frontend_candidates())
    return HTMLResponse(
        f"<h1>DGHub 前端资源缺失</h1><p>没有找到 src/frontend-vue/dist/index.html。</p><ul>{checked}</ul>",
        status_code=503,
    )
