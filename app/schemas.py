from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="after")
    def ensure_status_for_severe_cases(cls, model: "PlantHealthCreate"):
        if model.health_level != 1 and model.health_status is None:
            raise ValueError("health_status is required when health_level is not 1")

        return model


class PumpCommandCreate(BaseModel):
    water: bool = Field(default=True, description="Whether pump should activate")
    duration_seconds: Optional[int] = Field(
        default=3, ge=0, description="Duration for pump operation in seconds"
    )


class PumpCommandOut(BaseModel):
    command_id: Optional[int] = Field(default=None, description="Unique command id")
    water: bool
    duration_seconds: int
    issued_at: Optional[datetime]

    class Config:
        orm_mode = True
