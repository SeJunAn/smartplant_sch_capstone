from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class SensorDataCreate(BaseModel):
    soil_moisture: Optional[float] = Field(
        default=None, description="Soil moisture percentage"
    )
    temperature: Optional[float] = Field(
        default=None, description="Ambient temperature in Celsius"
    )
    humidity: Optional[float] = Field(
        default=None, description="Relative humidity percentage"
    )
    light_intensity: Optional[float] = Field(
        default=None, description="Light intensity level"
    )


class PumpLogCreate(BaseModel):
    start_time: Optional[datetime] = Field(
        default=None, description="Timestamp when the pump started"
    )


class PlantHealthCreate(BaseModel):
    health_level: int = Field(..., description="Numerical severity indicator")
    health_status: Optional[str] = Field(
        default=None, description="Diagnostic status label"
    )
    diagnosis_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the health status was recorded",
    )

    @root_validator
    def ensure_status_for_severe_cases(cls, values):
        level = values.get("health_level")
        status = values.get("health_status")

        if level != 1 and status is None:
            raise ValueError("health_status is required when health_level is not 1")

        return values
