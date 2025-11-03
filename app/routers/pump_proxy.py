import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PumpCommand
from app.schemas import PumpCommandCreate, PumpCommandOut

router = APIRouter(tags=["pump"])
logger = logging.getLogger(__name__)


@router.post("/pump-command", status_code=status.HTTP_201_CREATED)
def enqueue_pump_command(
    payload: PumpCommandCreate, db: Session = Depends(get_db)
):
    duration = payload.duration_seconds or 0
    command = PumpCommand(
        water=payload.water,
        duration_seconds=duration,
    )
    db.add(command)
    db.commit()
    db.refresh(command)

    logger.info(
        "Pump command enqueued",
        extra={
            "command_id": command.id,
            "water": command.water,
            "duration_seconds": command.duration_seconds,
        },
    )

    return {
        "detail": "Pump command registered.",
        "command_id": command.id,
        "issued_at": command.issued_at,
        "duration_seconds": command.duration_seconds,
        "water": command.water,
    }


@router.get("/pump-command", response_model=PumpCommandOut)
def dequeue_pump_command(db: Session = Depends(get_db)):
    command = (
        db.query(PumpCommand)
        .filter(PumpCommand.consumed_at.is_(None))
        .order_by(PumpCommand.issued_at.asc(), PumpCommand.id.asc())
        .with_for_update(skip_locked=True)
        .first()
    )

    if not command:
        return PumpCommandOut(
            command_id=None,
            water=False,
            duration_seconds=0,
            issued_at=None,
        )

    command.consumed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(command)

    logger.info(
        "Pump command dequeued",
        extra={
            "command_id": command.id,
            "water": command.water,
            "duration_seconds": command.duration_seconds,
        },
    )

    return PumpCommandOut(
        command_id=command.id,
        water=command.water,
        duration_seconds=command.duration_seconds,
        issued_at=command.issued_at,
    )
