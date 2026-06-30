from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/api")


@router.get("/ble/scan")
def ble_scan():
    return {"devices": []}
