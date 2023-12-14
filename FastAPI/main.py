from fastapi import Depends, FastAPI, HTTPException
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import get_db
from pydantic_models import PydanticCar
from database_models import SQLCar
import database_models
from database import engine


database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Routes

@app.get("/")
async def root():
    return {"message": "Hello World"}


# Passed

# endpoint: /cars and response model is list of PydanticCar
@app.get("/cars", response_model=list[PydanticCar])
async def read_cars(db: Session = Depends(get_db)):
    cars = db.query(SQLCar).all()
    return cars


@app.get('/car/{car_id}', response_model=PydanticCar)
async def read_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(SQLCar).filter(SQLCar.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.post("/car", response_model=PydanticCar)
async def create_car(car: PydanticCar, db: Session = Depends(get_db)):
    new_car = SQLCar(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@app.put("/car/{car_id}", response_model=PydanticCar)
async def update_car(car_id: int, car_update: PydanticCar, db: Session = Depends(get_db)):
    # Här fetchar vi från databasen
    db_car = db.query(SQLCar).filter(SQLCar.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    # Update car attributes
    for var, value in vars(car_update).items():
        setattr(db_car, var, value) if value is not None else None

    # Commit the changes
    db.commit()
    db.refresh(db_car)

    return db_car


# The response_model is set to dict as the operation does not return a Car model. Alternatively, you could set the status code to 204 and not return anything:
# vi förväntar oss 204 för deleted
@app.delete('/car/{car_id}', status_code=204)
async def read_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(SQLCar).filter(SQLCar.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}
