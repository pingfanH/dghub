from __future__ import annotations

import socket


def find_available_port(preferred: int, host: str = "127.0.0.1") -> int:
    for port in range(preferred, preferred + 100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
            except OSError:
                continue
            return port
    raise RuntimeError(f"No available port near {preferred}")


def get_local_ip() -> str:
    return "127.0.0.1"


def get_local_ip_by_interface(_interface: str | None = None) -> str:
    return get_local_ip()


def get_network_interfaces() -> list[dict[str, str]]:
    return [{"name": "localhost", "ip": "127.0.0.1"}]
