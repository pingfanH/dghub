from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/api")


@router.get("/status")
def status():
    return {"ok": True}
