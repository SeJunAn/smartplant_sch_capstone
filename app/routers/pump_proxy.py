import logging
import os
from typing import Any, Dict, Optional

import requests
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

FLASK_PUMP_URL = os.getenv(
    "FLASK_PUMP_URL", "http://192.168.223.55:5000/pump-command"
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["pump"])


class PumpCommandPayload(BaseModel):
    water: bool = Field(default=True, description="Whether to activate pump")
    duration_seconds: Optional[int] = Field(
        default=3, description="Desired pump duration in seconds"
    )

    class Config:
        extra = "allow"


@router.post("/pump-command", status_code=status.HTTP_202_ACCEPTED)
def forward_pump_command(payload: PumpCommandPayload) -> Dict[str, Any]:
    try:
        response = requests.post(
            FLASK_PUMP_URL,
            json=payload.dict(exclude_none=True),
            timeout=5,
        )
    except requests.RequestException as exc:
        logger.error("Failed to reach pump backend: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to reach internal pump controller.",
        ) from exc

    if response.status_code >= 400:
        logger.warning(
            "Pump backend returned error",
            extra={
                "status_code": response.status_code,
                "response_text": response.text[:200],
            },
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Pump controller responded with {response.status_code}",
        )

    logger.info("Pump command forwarded successfully")
    return {
        "detail": "Pump command forwarded successfully.",
        "pump_controller_status": response.status_code,
    }
