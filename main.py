from __future__ import annotations

import multiprocessing
import os
import socket
import sys
import threading
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
sys.argv[0] = str(ROOT / "main.py")
for path in (ROOT,):
    path_text = str(path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from macos_tcc_patch import apply_tcc_usage_descriptions
from pydglab_macos_patch import apply_patches
from src.api.app import app, _check_frontend_integrity, _find_frontend_path
from src.config.config_manager import ConfigManager
from src.runtime_flags import is_exit_confirmed
from src.utils.logger import get_logger
from src.utils.network import find_available_port


log = get_logger("Boot")
_main_server = None


def _get_port() -> int:
    try:
        preferred = int(ConfigManager().get_global("obs_port", 8000))
    except Exception:
        preferred = 8000
    return find_available_port(preferred)


def run_server(port: int) -> None:
    global _main_server
    import uvicorn

    access_log = os.environ.get("DGHUB_ACCESS_LOG", "").lower() in {"1", "true", "yes"}
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=port,
        log_level="info",
        reload=False,
        access_log=access_log,
    )
    _main_server = uvicorn.Server(config)
    _main_server.run()


def _wait_for_server(port: int, timeout: float = 15) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False


class _DesktopJsApi:
    def save_dev_guide(self):
        from src.utils.plugin_assets import dev_guide_path
        from src.utils.save_dialog import save_file_with_dialog

        return save_file_with_dialog(
            dev_guide_path(),
            "PLUGIN_DEVELOPMENT.md",
            ("Markdown (*.md)", "All files (*.*)"),
        )

    def save_demo_template(self):
        import os
        from src.utils.plugin_assets import build_demo_zip_file
        from src.utils.save_dialog import save_file_with_dialog

        tmp_path, _ = build_demo_zip_file()
        try:
            return save_file_with_dialog(
                tmp_path,
                "demo_external.zip",
                ("Zip archive (*.zip)", "All files (*.*)"),
            )
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def _check_frontend() -> None:
    frontend = _find_frontend_path()
    if frontend:
        missing = _check_frontend_integrity(frontend)
        if missing:
            log.warning(f"frontend integrity warning path={frontend} missing={missing[:5]}")
        else:
            log.info(f"frontend OK path={frontend}")
    else:
        log.warning("frontend dist NOT FOUND")


def start_desktop_app() -> None:
    import webview

    log.info("start_desktop_app: picking port")
    port = _get_port()
    os.environ["DGHUB_SERVER_PORT"] = str(port)

    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()
    ready = _wait_for_server(port)
    log.info(f"start_desktop_app: server ready={ready}")

    webview.settings["ALLOW_DOWNLOADS"] = True
    window = webview.create_window(
        "DGHub",
        f"http://127.0.0.1:{port}/static/index.html",
        width=1280,
        height=820,
        resizable=True,
        min_size=(960, 640),
        text_select=True,
        confirm_close=False,
        js_api=_DesktopJsApi(),
    )

    def _on_closing():
        if is_exit_confirmed():
            return True
        try:
            behavior = (ConfigManager().get_global("close_behavior") or "").strip()
        except Exception:
            behavior = ""
        if behavior == "exit":
            return True
        if behavior == "minimize":
            window.minimize()
            return False
        try:
            window.evaluate_js("window.dispatchEvent(new CustomEvent('confirm-close'))")
        except Exception:
            return True
        return False

    window.events.closing += _on_closing
    log.info("start_desktop_app: webview.start() entering GUI loop")
    webview.start()
    log.info("start_desktop_app: webview.start() returned")

    if _main_server:
        _main_server.should_exit = True
        server_thread.join(timeout=8)


def start_server() -> None:
    import uvicorn

    port = _get_port()
    os.environ["DGHUB_SERVER_PORT"] = str(port)
    print(f"DGHub 服务启动中 -> http://127.0.0.1:{port}")
    print(f"OBS 浏览器源地址 -> http://127.0.0.1:{port}/obs")
    access_log = os.environ.get("DGHUB_ACCESS_LOG", "").lower() in {"1", "true", "yes"}
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info", access_log=access_log)


def _maybe_run_overlay() -> bool:
    if "--overlay" not in sys.argv:
        return False
    from src.overlay.desktop_overlay import main as overlay_main

    overlay_main([arg for arg in sys.argv[1:] if arg != "--overlay"])
    return True


def _maybe_run_plugin_runner() -> bool:
    if "--plugin-runner" not in sys.argv:
        return False
    idx = sys.argv.index("--plugin-runner")
    if idx + 1 >= len(sys.argv):
        log.error("--plugin-runner 缺少脚本路径")
        sys.exit(2)
    from src.utils.plugin_runner import run_plugin_script

    run_plugin_script(sys.argv[idx + 1])
    return True


def main() -> None:
    multiprocessing.freeze_support()
    apply_tcc_usage_descriptions()
    log.info(f"=== DGHub macOS runtime starting === argv={sys.argv}")
    apply_patches()
    _check_frontend()

    if "--server" in sys.argv:
        start_server()
        return

    if _maybe_run_overlay():
        return

    if _maybe_run_plugin_runner():
        return

    from src.utils.single_instance import try_acquire_desktop_instance

    if not try_acquire_desktop_instance():
        return
    start_desktop_app()


if __name__ == "__main__":
    main()
