from __future__ import annotations

import asyncio
import json

from fastapi import WebSocket, WebSocketDisconnect

from src.api.state import state
from src.api.status_payload import collect_status_payload


async def broadcast(data: dict) -> None:
    async with state._ws_lock:
        connections = list(state.websocket_connections)

    if not connections:
        return

    payload = json.dumps(data, ensure_ascii=False)
    results = await asyncio.gather(
        *(websocket.send_text(payload) for websocket in connections),
        return_exceptions=True,
    )
    dead = {
        websocket
        for websocket, result in zip(connections, results)
        if isinstance(result, Exception)
    }
    if dead:
        async with state._ws_lock:
            state.websocket_connections.difference_update(dead)


async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    async with state._ws_lock:
        state.websocket_connections.add(websocket)

    try:
        await websocket.send_text(json.dumps({"type": "hello"}, ensure_ascii=False))
        payload = collect_status_payload()
        await websocket.send_text(
            json.dumps(
                {"type": "status_update", "data": payload or _fallback_status_payload()},
                ensure_ascii=False,
            )
        )
        ping_task = asyncio.create_task(_ping_loop(websocket))
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            ping_task.cancel()
            await asyncio.gather(ping_task, return_exceptions=True)
    finally:
        async with state._ws_lock:
            state.websocket_connections.discard(websocket)


async def _ping_loop(websocket: WebSocket) -> None:
    while True:
        await asyncio.sleep(15)
        await websocket.send_text(json.dumps({"type": "ping"}))


def _fallback_status_payload() -> dict:
    return {
        "device_type": state.device_type,
        "strength_a": state.strength_a,
        "strength_b": state.strength_b,
        "max_strength_A": state.max_strength_A,
        "max_strength_B": state.max_strength_B,
        "plugins": state.plugins_status,
        "qrcode_path": state.qrcode_path,
    }
