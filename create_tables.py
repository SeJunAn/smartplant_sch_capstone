from app.database import engine, Base
from app.models import SensorData, PumpLog, PlantHealth

print("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
