from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from database_models import SQLCar

DATABASE_URL = "postgresql://postgres:Vanligt123!@localhost/carappdb"

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

# No test
# try:
#     # här försöker nå till databasen och få ett meddelande ifall vi lyckades eller inte
#     with engine.connect() as connection:
#         result = connection.execute(SQLCar)
#         for row in result:
#             print(row)
#     print("Database connection was successful.")
# except Exception as e:
#     print("Error connecting to the database:", e)

# Use this dependency in your route handlers
