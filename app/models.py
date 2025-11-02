from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base
from datetime import datetime

# 1️⃣ 센서 데이터
class SensorData(Base):
    __tablename__ = "SensorData"

    id = Column(Integer, primary_key=True, index=True)
    soil_moisture = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    light_intensity = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


# 2️⃣ 펌프 작동 로그
class PumpLog(Base):
    __tablename__ = "PumpLog"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)


# 3️⃣ 식물 건강 상태
class PlantHealth(Base):
    __tablename__ = "PlantHealth"

    id = Column(Integer, primary_key=True, index=True)
    health_level = Column(Integer, nullable=False)
    health_status = Column(String(100), nullable=False)
    diagnosis_date = Column(DateTime, default=datetime.utcnow)
