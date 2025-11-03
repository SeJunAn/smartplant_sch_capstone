import logging
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, Optional

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(tags=["pump"])


class PumpCommandPayload(BaseModel):
    water: bool = Field(default=True, description="Whether to activate pump")
    duration_seconds: Optional[int] = Field(
        default=3, description="Desired pump duration in seconds"
    )

    class Config:
        extra = "allow"


class PumpCommandResponse(BaseModel):
    water: bool
    duration_seconds: int = 0
    issued_at: Optional[str] = None


_command_lock: Lock = Lock()
_latest_command: Dict[str, Any] = {}


def _set_command(payload: PumpCommandPayload) -> Dict[str, Any]:
    with _command_lock:
        command = {
            "water": payload.water,
            "duration_seconds": payload.duration_seconds or 0,
            "issued_at": datetime.now(timezone.utc).isoformat(),
        }
        global _latest_command
        _latest_command = command
        return command


def _pop_command() -> Dict[str, Any]:
    with _command_lock:
        global _latest_command
        if not _latest_command:
            return {"water": False, "duration_seconds": 0, "issued_at": None}

        command = _latest_command
        # Clear after single consumption so repeated polling doesn't retrigger.
        _latest_command = {}
        return command


@router.post("/pump-command", status_code=status.HTTP_202_ACCEPTED)
def create_pump_command(payload: PumpCommandPayload) -> Dict[str, Any]:
    command = _set_command(payload)
    logger.info(
        "Pump command queued",
        extra={
            "water": command["water"],
            "duration_seconds": command["duration_seconds"],
            "issued_at": command["issued_at"],
        },
    )

    return {
        "detail": "Pump command registered.",
        "command": command,
    }


@router.get("/pump-command", response_model=PumpCommandResponse)
def fetch_pump_command() -> PumpCommandResponse:
    command = _pop_command()
    logger.info("Pump command retrieved", extra={"water": command["water"]})
    return PumpCommandResponse(**command)
