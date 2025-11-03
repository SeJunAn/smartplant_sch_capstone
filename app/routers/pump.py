from datetime import datetime, timezone
import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PumpLog
from app.schemas import PumpLogCreate

router = APIRouter(prefix="/pump-log", tags=["pump-log"])
logger = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pump_log(
    payload: PumpLogCreate, db: Session = Depends(get_db)
):
    start_time = payload.start_time or datetime.now(timezone.utc)

    pump_log = PumpLog(start_time=start_time)

    db.add(pump_log)
    db.commit()
    db.refresh(pump_log)

    logger.info(
        "Pump log entry created",
        extra={
            "pump_log_id": pump_log.id,
            "start_time": pump_log.start_time.isoformat(),
        },
    )

    return {
        "id": pump_log.id,
        "start_time": pump_log.start_time,
    }
