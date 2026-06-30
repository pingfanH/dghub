from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.frontend_guard import _check_frontend_integrity, _find_frontend_path, _serve_index_or_diagnostic
from src.api.state import state
from src.api.websocket import websocket_endpoint
from src.config.config_manager import ConfigManager


class PresetManager:
    def __init__(self, _base_path=None) -> None:
        self.presets = {}


app = FastAPI(title="DGHub 控制中心")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = ConfigManager()
preset_manager = PresetManager(config.config_path.parent)


@app.get("/")
@app.get("/static/index.html")
def index():
    return _serve_index_or_diagnostic()


@app.get("/obs")
def obs():
    frontend = _find_frontend_path()
    if frontend and (frontend / "obs.html").exists():
        from fastapi.responses import HTMLResponse

        return HTMLResponse((frontend / "obs.html").read_text(encoding="utf-8"))
    return _serve_index_or_diagnostic()


@app.get("/api/status")
def status():
    return {
        "ok": True,
        "device_type": state.device_type,
        "strength": {"a": state.strength_a, "b": state.strength_b},
        "plugins": state.plugins_status,
    }


frontend_path = _find_frontend_path()
if frontend_path:
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.add_api_websocket_route("/ws", websocket_endpoint)
