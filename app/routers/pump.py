from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PumpLog
from app.schemas import PumpLogCreate

router = APIRouter(prefix="/pump-log", tags=["pump-log"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pump_log(
    payload: PumpLogCreate, db: Session = Depends(get_db)
):
    start_time = payload.start_time or datetime.utcnow()

    pump_log = PumpLog(start_time=start_time)

    db.add(pump_log)
    db.commit()
    db.refresh(pump_log)

    return {
        "id": pump_log.id,
        "start_time": pump_log.start_time,
    }
