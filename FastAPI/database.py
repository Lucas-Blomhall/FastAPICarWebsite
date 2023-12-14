from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from database_models import SQLCar

DATABASE_URL = "postgresql://postgres:YourPassword@localhost/carappdb"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Alltid i slutet: "Base.metadata.create_all(bind=engine)" Den skapar tabellen i databasen.
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
