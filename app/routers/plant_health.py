from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PlantHealth
from app.schemas import PlantHealthCreate

router = APIRouter(prefix="/plant-health", tags=["plant-health"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_plant_health(
    payload: PlantHealthCreate, db: Session = Depends(get_db)
):
    status_value = payload.health_status or "Healthy"

    health_record = PlantHealth(
        health_level=payload.health_level,
        health_status=status_value,
        diagnosis_date=payload.diagnosis_date,
    )
    db.add(health_record)
    db.commit()
    db.refresh(health_record)

    return {
        "id": health_record.id,
        "health_level": health_record.health_level,
        "health_status": health_record.health_status,
        "diagnosis_date": health_record.diagnosis_date,
    }
