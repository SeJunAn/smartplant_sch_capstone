from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


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
