from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any


class ConfigManager:
    def __init__(self, config_path: str | Path = "config.json") -> None:
        self.config_path = Path(config_path)
        if not self.config_path.is_absolute():
            self.config_path = Path.cwd() / self.config_path
        self._lock = threading.Lock()
        self.config: dict[str, Any] = {"global": {}, "plugins": {}}
        self._load_config()

    def _load_config(self) -> None:
        if not self.config_path.exists():
            self._save()
            return
        try:
            self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        except Exception:
            self.config = {"global": {}, "plugins": {}}
        self.config.setdefault("global", {})
        self.config.setdefault("plugins", {})

    def _save(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_global(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self.config.get("global", {}).get(key, default)

    def set_global(self, key: str, value: Any) -> None:
        with self._lock:
            self.config.setdefault("global", {})[key] = value
            self._save()

    def get_plugin(self, plugin_name: str, key: str, default: Any = None) -> Any:
        with self._lock:
            return self.config.get("plugins", {}).get(plugin_name, {}).get(key, default)

    def get_plugin_config(self, plugin_name: str) -> dict[str, Any]:
        with self._lock:
            return dict(self.config.get("plugins", {}).get(plugin_name, {}))

    def set_plugin(self, plugin_name: str, key: str, value: Any) -> None:
        with self._lock:
            self.config.setdefault("plugins", {}).setdefault(plugin_name, {})[key] = value
            self._save()
