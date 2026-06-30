from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from urllib import request as urlreq
from urllib.parse import urlencode

from PyQt6.QtCore import QObject, QRect, Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtGui import QColor, QGuiApplication, QPalette
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QFrame, QSizeGrip, QVBoxLayout, QWidget


TRANSPARENT = QColor(0, 0, 0, 0)
MACOS_COLLECTION_BEHAVIOR_NAMES = (
    "NSWindowCollectionBehaviorCanJoinAllSpaces",
    "NSWindowCollectionBehaviorFullScreenAuxiliary",
    "NSWindowCollectionBehaviorStationary",
    "NSWindowCollectionBehaviorIgnoresCycle",
)


def _macos_collection_behavior_mask(appkit) -> int:
    mask = 0
    for name in MACOS_COLLECTION_BEHAVIOR_NAMES:
        mask |= int(getattr(appkit, name, 0))
    return mask


class ControlClient(QObject):
    command = pyqtSignal(str, str)

    def __init__(self, base_url: str, token: str, poll_ms: int = 500) -> None:
        super().__init__()
        self._base = base_url.rstrip("/")
        self._token = token
        self._poll = poll_ms / 1000.0
        self._stop = False

    def start(self) -> None:
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self) -> None:
        self._stop = True

    def _loop(self) -> None:
        misses = 0
        while not self._stop:
            try:
                url = f"{self._base}/api/overlay/_pending_cmd?{urlencode({'token': self._token})}"
                with urlreq.urlopen(url, timeout=2) as response:
                    data = json.loads(response.read().decode("utf-8"))
                misses = 0
                for item in data.get("commands", []):
                    cmd = item.get("cmd", "")
                    arg = item.get("arg", "")
                    if cmd:
                        self.command.emit(cmd, str(arg))
            except Exception:
                misses += 1
                if misses > 30:
                    self.command.emit("exit", "")
                    return
            time.sleep(self._poll)

    def report(self, payload: dict) -> None:
        try:
            url = f"{self._base}/api/overlay/_report?{urlencode({'token': self._token})}"
            req = urlreq.Request(
                url,
                json.dumps(payload).encode("utf-8"),
                {"Content-Type": "application/json"},
                method="POST",
            )
            urlreq.urlopen(req, timeout=2).close()
        except Exception:
            pass


class OverlayWindow(QWidget):
    EDIT_CARD_QSS = """
        QFrame#edit_card {
            background: rgba(255, 255, 255, 28);
            border: 1px dashed rgba(34, 211, 238, 190);
            border-radius: 8px;
        }
    """

    def __init__(
        self,
        url: str,
        x: int,
        y: int,
        width: int,
        height: int,
        opacity: float,
        locked: bool,
        control: ControlClient,
    ) -> None:
        super().__init__()
        self.setObjectName("root")
        self._control = control
        self._locked = False
        self._drag_origin = None

        flags = (
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.NoDropShadowWindowHint
        )
        no_focus_flag = getattr(Qt.WindowType, "WindowDoesNotAcceptFocus", None)
        if no_focus_flag is not None:
            flags |= no_focus_flag
        self.setWindowFlags(flags)
        self._force_transparent_widget(self)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        if hasattr(Qt.WidgetAttribute, "WA_MacAlwaysShowToolWindow"):
            self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow, True)
        self.setWindowOpacity(max(0.1, min(1.0, opacity)))
        self.setGeometry(x, y, width, height)

        self._view = QWebEngineView(self)
        self._view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._force_transparent_widget(self._view)
        self._view.page().setBackgroundColor(TRANSPARENT)
        self._view.setStyleSheet("background: transparent; border: 0;")

        separator = "&" if "?" in url else "?"
        self._view.load(QUrl(f"{url}{separator}desktop=1"))

        settings = self._view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._view)

        self._edit_card = QFrame(self)
        self._edit_card.setObjectName("edit_card")
        self._edit_card.setStyleSheet(self.EDIT_CARD_QSS)
        self._edit_card.hide()

        self._grip = QSizeGrip(self)
        self._grip.setFixedSize(16, 16)
        self._grip.hide()

        control.command.connect(self._handle_cmd)

        self._report_timer = QTimer(self)
        self._report_timer.setSingleShot(True)
        self._report_timer.timeout.connect(self._report_geometry)

        QTimer.singleShot(0, lambda: self.set_locked(locked))
        self._schedule_macos_window_behavior()

    @staticmethod
    def _force_transparent_widget(widget: QWidget) -> None:
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        widget.setAutoFillBackground(False)
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.Window, TRANSPARENT)
        palette.setColor(QPalette.ColorRole.Base, TRANSPARENT)
        widget.setPalette(palette)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._schedule_macos_window_behavior()

    def changeEvent(self, event) -> None:
        super().changeEvent(event)
        self._schedule_macos_window_behavior()

    def _schedule_macos_window_behavior(self) -> None:
        if sys.platform != "darwin":
            return
        QTimer.singleShot(0, self._apply_macos_window_behavior)
        QTimer.singleShot(250, self._apply_macos_window_behavior)

    def _apply_macos_window_behavior(self) -> None:
        if sys.platform != "darwin":
            return
        try:
            import AppKit
            import objc

            native = objc.objc_object(c_void_p=int(self.winId()))
            window = native.window() if native.respondsToSelector_(b"window") else native
            if not window:
                return

            behavior = int(window.collectionBehavior()) | _macos_collection_behavior_mask(AppKit)
            window.setCollectionBehavior_(behavior)
            window.setLevel_(int(getattr(AppKit, "NSStatusWindowLevel", AppKit.NSFloatingWindowLevel)))
            window.setReleasedWhenClosed_(False)
            if window.respondsToSelector_(b"setIgnoresMouseEvents:"):
                window.setIgnoresMouseEvents_(bool(self._locked))
        except Exception:
            pass

    def set_locked(self, locked: bool) -> None:
        self._locked = locked
        was_visible = self.isVisible()
        self.setWindowFlag(Qt.WindowType.WindowTransparentForInput, locked)
        self._apply_visuals()
        if was_visible:
            self.show()
        self.clearFocus()
        self._view.clearFocus()
        self._schedule_macos_window_behavior()

    def _apply_visuals(self) -> None:
        self._force_transparent_widget(self)
        self._force_transparent_widget(self._view)
        self._view.page().setBackgroundColor(TRANSPARENT)

        if self._locked:
            self._edit_card.hide()
            self._view.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            self._grip.hide()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            return

        self._edit_card.setGeometry(0, 0, self.width(), self.height())
        self._edit_card.show()
        self._edit_card.raise_()
        self._view.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setCursor(Qt.CursorShape.SizeAllCursor)
        self._grip.show()
        self._reposition_grip()
        self._grip.raise_()

    def _reposition_grip(self) -> None:
        self._grip.move(max(0, self.width() - 18), max(0, self.height() - 18))

    def mousePressEvent(self, event) -> None:
        if not self._locked and event.button() == Qt.MouseButton.LeftButton:
            self._drag_origin = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event) -> None:
        if not self._locked and self._drag_origin is not None:
            self.move(event.globalPosition().toPoint() - self._drag_origin)
            self._schedule_report()

    def mouseReleaseEvent(self, event) -> None:
        self._drag_origin = None
        self._report_geometry()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._apply_visuals()
        self._schedule_report()

    def _schedule_report(self) -> None:
        self._report_timer.start(250)

    def _report_geometry(self) -> None:
        self._control.report(
            {
                "x": self.x(),
                "y": self.y(),
                "width": self.width(),
                "height": self.height(),
                "locked": self._locked,
                "opacity": self.windowOpacity(),
            }
        )

    def _handle_cmd(self, cmd: str, arg: str) -> None:
        if cmd == "lock":
            self.set_locked(True)
            self._report_geometry()
        elif cmd == "unlock":
            self.set_locked(False)
            self._report_geometry()
        elif cmd == "toggle":
            self.set_locked(not self._locked)
            self._report_geometry()
        elif cmd == "opacity":
            try:
                self.setWindowOpacity(max(0.1, min(1.0, float(arg))))
                self._report_geometry()
            except ValueError:
                pass
        elif cmd == "geometry":
            try:
                geom = json.loads(arg)
                self.setGeometry(
                    int(geom["x"]),
                    int(geom["y"]),
                    int(geom["width"]),
                    int(geom["height"]),
                )
            except Exception:
                pass
        elif cmd == "exit":
            self._control.stop()
            QApplication.quit()

    def keep_visible_on_current_space(self) -> None:
        self._apply_macos_window_behavior()
        if not self.isVisible():
            self.show()
            self.clearFocus()
            self._view.clearFocus()


def _clamp_to_screens(x: int, y: int, width: int, height: int) -> tuple[int, int, int, int]:
    screens = QGuiApplication.screens()
    if not screens:
        return x, y, width, height
    target = QRect(x, y, width, height)
    for screen in screens:
        if screen.geometry().intersects(target):
            return x, y, width, height
    primary = QGuiApplication.primaryScreen().availableGeometry()
    return primary.x() + primary.width() - width - 20, primary.y() + 20, width, height


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="dghub-overlay", add_help=False)
    parser.add_argument("--url", required=True)
    parser.add_argument("--control-url", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--x", type=int, default=-1)
    parser.add_argument("--y", type=int, default=-1)
    parser.add_argument("--width", type=int, default=560)
    parser.add_argument("--height", type=int, default=420)
    parser.add_argument("--opacity", type=float, default=1.0)
    parser.add_argument("--locked", action="store_true")
    args, _unknown = parser.parse_known_args(argv)

    app = QApplication(sys.argv[:1])
    app.setQuitOnLastWindowClosed(True)
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.Window, TRANSPARENT)
    palette.setColor(QPalette.ColorRole.Base, TRANSPARENT)
    app.setPalette(palette)

    if args.x < 0 or args.y < 0:
        primary = QGuiApplication.primaryScreen().availableGeometry()
        args.x = primary.x() + primary.width() - args.width - 20
        args.y = primary.y() + 20
    else:
        args.x, args.y, args.width, args.height = _clamp_to_screens(
            args.x,
            args.y,
            args.width,
            args.height,
        )

    control = ControlClient(args.control_url, args.token)
    win = OverlayWindow(
        args.url,
        args.x,
        args.y,
        args.width,
        args.height,
        args.opacity,
        args.locked,
        control,
    )
    control.start()
    win.show()
    if sys.platform == "darwin":
        keep_visible = lambda *_args: win.keep_visible_on_current_space()
        app.applicationStateChanged.connect(keep_visible)
        app.screenAdded.connect(keep_visible)
        app.screenRemoved.connect(keep_visible)
        app.primaryScreenChanged.connect(keep_visible)
        if QGuiApplication.primaryScreen():
            QGuiApplication.primaryScreen().geometryChanged.connect(keep_visible)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
