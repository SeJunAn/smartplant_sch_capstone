from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SensorData
from app.schemas import SensorDataCreate

router = APIRouter(prefix="/sensor-data", tags=["sensor-data"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_sensor_data(
    payload: SensorDataCreate, db: Session = Depends(get_db)
):
    payload_dict = payload.dict()
    if all(value is None for value in payload_dict.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one sensor value must be provided.",
        )

    sensor_record = SensorData(**payload_dict)
    db.add(sensor_record)
    db.commit()
    db.refresh(sensor_record)

    return {
        "id": sensor_record.id,
        "soil_moisture": sensor_record.soil_moisture,
        "temperature": sensor_record.temperature,
        "humidity": sensor_record.humidity,
        "light_intensity": sensor_record.light_intensity,
        "timestamp": sensor_record.timestamp,
    }
