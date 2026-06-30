from __future__ import annotations

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.frontend_guard import _check_frontend_integrity, _find_frontend_path, _serve_index_or_diagnostic
from src.api.state import state
from src.api.status_payload import collect_status_payload
from src.api.websocket import websocket_endpoint
from src.config.config_manager import ConfigManager
from src.version import __version__


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
    return collect_status_payload()


@app.get("/api/device-type")
def get_device_type():
    return {"status": "success", "device_type": state.device_type}


@app.post("/api/device-type")
async def set_device_type(request: Request):
    data = await request.json()
    state.device_type = data.get("device_type", state.device_type)
    return {"status": "success", "device_type": state.device_type}


@app.get("/api/plugins")
def get_plugins():
    return {"status": "success", "plugins": []}


@app.get("/api/plugins/_plugins_dir")
def get_plugins_dir():
    return {"status": "success", "path": str((ConfigManager().config_path.parent / "plugins").resolve())}


@app.get("/api/plugins/_session_token")
def get_plugin_session_token():
    return {"status": "success", "token": state.plugin_session_token}


@app.post("/api/plugins/{plugin_name}/toggle")
async def toggle_plugin(plugin_name: str, request: Request):
    data = await request.json()
    return {"status": "success", "plugin": plugin_name, "enabled": bool(data.get("enabled"))}


@app.get("/api/logs")
def get_logs():
    try:
        from src.utils.logger import memory_handler

        logs = memory_handler.get_logs()
    except Exception:
        logs = []
    return {"status": "success", "logs": logs}


@app.get("/api/config")
def get_config():
    return {"status": "success", "config": config.config}


@app.post("/api/config")
async def set_config(request: Request):
    data = await request.json()
    if isinstance(data, dict):
        config.config.update(data)
        config._save()
    return {"status": "success", "config": config.config}


@app.post("/api/config/plugin/{plugin_name}")
async def set_plugin_config(plugin_name: str, request: Request):
    data = await request.json()
    config.config.setdefault("plugins", {})[plugin_name] = data
    config._save()
    return {"status": "success", "config": data}


@app.get("/api/version")
def get_version():
    return {"version": __version__}


@app.get("/api/update/check")
def check_update():
    return {"update_status": "none"}


@app.post("/api/update/download")
def download_update():
    return {"status": "success", "update_status": "none"}


@app.post("/api/update/apply")
def apply_update():
    return {"status": "success", "update_status": "none"}


@app.get("/api/update/status")
def update_status():
    return {"status": "success", "update_status": "none"}


@app.get("/api/overlay/config")
def overlay_config():
    cfg = config.config.setdefault("global", {}).setdefault(
        "overlay",
        {"enabled": False, "x": -1, "y": -1, "width": 560, "height": 420, "opacity": 1, "locked": False},
    )
    return {"status": "success", "config": cfg}


@app.get("/api/overlay/status")
def overlay_status():
    return {"status": "success", "running": False}


@app.post("/api/overlay/start")
def overlay_start():
    return {"status": "success", "running": False}


@app.post("/api/overlay/stop")
def overlay_stop():
    return {"status": "success", "running": False}


@app.get("/api/ble/scan")
def ble_scan():
    return {"status": "success", "devices": []}


@app.post("/api/ble/connect")
async def ble_connect(_request: Request):
    return {"status": "error", "message": "BLE source implementation is not restored yet"}


@app.post("/api/ble/disconnect")
def ble_disconnect():
    return {"status": "success"}


frontend_path = _find_frontend_path()
if frontend_path:
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.add_api_websocket_route("/ws", websocket_endpoint)
