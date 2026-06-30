from __future__ import annotations

import logging
import logging.handlers
import sys
import traceback
from collections import deque
from datetime import datetime
from pathlib import Path


def _get_log_dir() -> Path:
    base = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path.cwd()
    log_dir = base / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        probe = log_dir / ".write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return log_dir
    except OSError:
        import tempfile

        fallback = Path(tempfile.gettempdir()) / "DGHub" / "logs"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


class MemoryLogHandler(logging.Handler):
    def __init__(self, capacity: int = 1000) -> None:
        super().__init__()
        self.records: deque[str] = deque(maxlen=capacity)

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(self.format(record))

    def get_logs(self) -> list[str]:
        return list(self.records)


memory_handler = MemoryLogHandler()
memory_handler.setFormatter(logging.Formatter("%(message)s"))

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
if memory_handler not in root_logger.handlers:
    root_logger.addHandler(memory_handler)

if not any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers):
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%H:%M:%S")
    )
    root_logger.addHandler(console_handler)

try:
    _log_dir = _get_log_dir()
    _log_file = _log_dir / "app.log"
    file_handler = logging.handlers.RotatingFileHandler(
        _log_file,
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )
    root_logger.addHandler(file_handler)

    def _excepthook(exc_type, exc_value, exc_tb):
        with (_log_dir / "crash.log").open("a", encoding="utf-8") as handle:
            handle.write(f"\n===== {datetime.now().isoformat()} =====\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=handle)
        sys.__excepthook__(exc_type, exc_value, exc_tb)

    sys.excepthook = _excepthook
except Exception:
    pass


def get_logger(name: str = "DGHub") -> logging.Logger:
    return logging.getLogger(name)
