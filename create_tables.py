from app.database import Base, engine
from app import models  # noqa: F401  pylint: disable=unused-import

def create_tables():
    print("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
