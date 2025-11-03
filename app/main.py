from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.routers import image_proxy, plant_health, pump, sensor
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
        last_watered = latest_data.timestamp or datetime.now(timezone.utc)
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

    return templates.TemplateResponse(
        "index.html", {"request": request, **sensor_data}
    )
