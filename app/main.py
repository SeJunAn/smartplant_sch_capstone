from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import example


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 라우터 등록
app.include_router(example.router)

# 템플릿 설정
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    sensor_data = {
        "temperature": 23.4,
        "moisture": 41.2,
        "humidity": 62,
        "light": 812,
        "last_watered": "2025-10-16 14:32",
        "status": "Healthy"
    }
    return templates.TemplateResponse(
        "index.html",
        {"request": request, **sensor_data}
    )