import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from app.routers import image_proxy, plant_health, pump, pump_proxy, sensor
from app.database import get_db
from app.models import SensorData

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# 정적 파일 등록
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(sensor.router)
app.include_router(pump.router)
app.include_router(plant_health.router)
app.include_router(image_proxy.router)
app.include_router(pump_proxy.router)

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request, db: Session = Depends(get_db)):
    latest_data = (
        db.query(SensorData)
        .order_by(SensorData.timestamp.desc())
        .first()
    )

    def _format_value(value: Optional[float]) -> str:
        return f"{value:.1f}" if value is not None else "-"

    if latest_data:
        moisture = latest_data.soil_moisture
        status = "Needs Water" if (moisture is not None and moisture < 30) else "Healthy"
        record_time = latest_data.timestamp or datetime.now(timezone.utc)
        if record_time.tzinfo is None:
            record_time = record_time.replace(tzinfo=timezone.utc)
        last_watered = record_time.astimezone(ZoneInfo("Asia/Seoul"))
        sensor_data = {
            "temperature": _format_value(latest_data.temperature),
            "moisture": _format_value(moisture),
            "humidity": _format_value(latest_data.humidity),
            "light": _format_value(latest_data.light_intensity),
            "last_watered": last_watered.strftime("%Y-%m-%d %H:%M"),
            "status": status,
        }
    else:
        sensor_data = {
            "temperature": "-",
            "moisture": "-",
            "humidity": "-",
            "light": "-",
            "last_watered": "데이터 없음",
            "status": "Waiting for sensor data",
        }

    pump_command_endpoint = os.getenv("PUMP_COMMAND_ENDPOINT")
    if not pump_command_endpoint:
        pump_command_endpoint = request.app.url_path_for("enqueue_pump_command")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            **sensor_data,
            "pump_command_endpoint": pump_command_endpoint,
        },
    )
