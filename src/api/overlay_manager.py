from __future__ import annotations

import atexit
import secrets
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from src.utils.logger import get_logger
from src.utils.process_kit import spawn_managed_subprocess


logger = get_logger("OverlayManager")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path.cwd()
OVERLAY_LOG = RUNTIME_ROOT / "logs" / "overlay-subprocess.log"

DEFAULT_CONFIG = {
    "enabled": False,
    "x": -1,
    "y": -1,
    "width": 560,
    "height": 420,
    "opacity": 1.0,
    "locked": False,
}


def normalize_config(cfg: Any = None) -> dict:
    if not isinstance(cfg, dict):
        cfg = {}
    out = dict(DEFAULT_CONFIG)
    out.update({k: v for k, v in cfg.items() if k in DEFAULT_CONFIG})
    out["opacity"] = max(0.1, min(1.0, float(out.get("opacity", 1.0))))
    out["width"] = max(120, int(out.get("width", 560)))
    out["height"] = max(80, int(out.get("height", 420)))
    return out


class OverlayManager:
    def __init__(self) -> None:
        self._proc: subprocess.Popen | None = None
        self._token = ""
        self._cmd_queue: list[dict] = []
        self._lock = threading.Lock()
        self._start_lock = threading.Lock()
        self._last_geometry: dict = {}
        self._last_returncode: int | None = None

    def is_running(self) -> bool:
        proc = self._proc
        if proc is None:
            return False
        returncode = proc.poll()
        if returncode is None:
            return True
        if self._last_returncode != returncode:
            self._last_returncode = returncode
            logger.warning(f"desktop overlay exited pid={proc.pid} returncode={returncode}; see {OVERLAY_LOG}")
        return False

    def start(self, server_port: int, cfg: dict | None = None) -> bool:
        with self._start_lock:
            if self.is_running():
                return True

            cfg = normalize_config(cfg)
            cfg["locked"] = True
            self._token = secrets.token_urlsafe(16)
            self._cmd_queue = []
            self._last_geometry = {}
            self._last_returncode = None
            argv = self._build_argv(server_port, cfg)

            try:
                OVERLAY_LOG.parent.mkdir(parents=True, exist_ok=True)
                with OVERLAY_LOG.open("ab") as log_file:
                    log_file.write(b"\n===== overlay subprocess start =====\n")
                    log_file.write(("argv=" + repr(argv) + "\n").encode("utf-8", "replace"))
                    log_file.flush()
                    self._proc = spawn_managed_subprocess(
                        argv,
                        stdin=subprocess.DEVNULL,
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        close_fds=True,
                        cwd=str(RUNTIME_ROOT),
                    )
                logger.info(f"桌面悬浮窗已启动 pid={self._proc.pid}")
                return True
            except Exception as exc:
                logger.error(f"桌面悬浮窗启动失败: {exc}")
                self._proc = None
                return False

    def stop(self, timeout: float = 2.0) -> None:
        proc = self._proc
        self._proc = None
        if not proc or proc.poll() is not None:
            return

        with self._lock:
            self._cmd_queue.append({"cmd": "exit", "arg": ""})

        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                proc.terminate()
                proc.wait(timeout=1.0)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        logger.info("桌面悬浮窗已关闭")

    def _build_argv(self, server_port: int, cfg: dict) -> list[str]:
        url = f"http://127.0.0.1:{server_port}/obs"
        control_url = f"http://127.0.0.1:{server_port}"
        if getattr(sys, "frozen", False):
            base = [sys.executable]
        else:
            base = [sys.executable, str(PROJECT_ROOT / "main.py")]

        argv = base + [
            "--overlay",
            "--url",
            url,
            "--control-url",
            control_url,
            "--token",
            self._token,
            "--width",
            str(cfg["width"]),
            "--height",
            str(cfg["height"]),
            "--opacity",
            f"{cfg['opacity']:.3f}",
        ]
        if cfg.get("x", -1) >= 0 and cfg.get("y", -1) >= 0:
            argv += ["--x", str(cfg["x"]), "--y", str(cfg["y"])]
        if cfg.get("locked"):
            argv.append("--locked")
        return argv

    def queue_command(self, cmd: str, arg: str = "") -> bool:
        if not self.is_running():
            return False
        with self._lock:
            self._cmd_queue.append({"cmd": cmd, "arg": str(arg)})
        return True

    def pop_pending(self, token: str) -> list[dict]:
        if token != self._token or not self._token:
            return []
        with self._lock:
            cmds = self._cmd_queue
            self._cmd_queue = []
        return cmds

    def update_geometry(self, token: str, payload: dict) -> bool:
        if token != self._token or not self._token:
            return False
        clean = {}
        for key in ("x", "y", "width", "height", "locked", "opacity"):
            if key in payload:
                clean[key] = payload[key]
        self._last_geometry = clean
        return True

    def get_last_geometry(self) -> dict:
        return dict(self._last_geometry)


_overlay_manager: OverlayManager | None = None


def get_overlay_manager() -> OverlayManager:
    global _overlay_manager
    if _overlay_manager is None:
        _overlay_manager = OverlayManager()
        atexit.register(_atexit_kill_overlay)
    return _overlay_manager


def _atexit_kill_overlay() -> None:
    mgr = _overlay_manager
    if mgr is None:
        return
    try:
        if mgr.is_running():
            mgr.stop(timeout=0.5)
    except Exception:
        pass
