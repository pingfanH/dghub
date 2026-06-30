from __future__ import annotations


class AdapterManager:
    def __init__(self, *_args, **_kwargs) -> None:
        self.adapters = {}

    def list_adapters(self):
        return list(self.adapters)
