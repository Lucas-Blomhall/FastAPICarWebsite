from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
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


@app.post("/cars", response_model=PydanticCar)
async def create_car(car: PydanticCar, db: Session = Depends(get_db)):
    new_car = SQLCar(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@app.put("/cars/{car_id}", response_model=PydanticCar)
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


@app.delete("/cars/{car_id}", response_model=PydanticCar)
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


# # update car

# @app.patch("/cars/{car_id}", response_model=PydanticCar)
# async def update_car(car_id: int, car: SQLCar, db: Session = Depends(get_db)):
#     db_car = SQLCar.model_validate(car)
#     db.add(db_car)
#     db.commit()
#     db.refresh(db_car)
#     return db_car


# @app.put("/cars/{car_id}", response_model=PydanticCar)
# async def update_item(car_id: int, car: SQLCar):
#     cars[car_id] = car
#     return car


# #first code from stackoverflow and tiangolo
# @app.patch("/cars/{car_id}", response_model=PydanticCar)
# async def update_car(car_id: int, car: SQLCar, db: Session = Depends(get_db)):
#     db_car = SQLCar.model_validate(car)
#     db.add(db_car)
#     db.commit()
#     db.refresh(db_car)
#     return db_car

    # extra code i saw on the internet
    # update_car_encoded = jsonable_encoder(car)
    # cars[car_id] = update_car_encoded
    # return update_car_encoded


# _car = SQLCar(car_name=car.car_name, price=car.price, year=car.year,
#                   car_type=car.car_type, engine_type=car.engine_type)

# @app.get("/cars", response_model=list[PydanticCar])
# async def get_car_by_id(db: Session = Depends(get_db), car_id: int):
#     return db.query(SQLCar).filter(SQLCar.id == car_id).first()


# older code below


# @app.get("/cars")
# def read_cars(db: Session = Depends(get_db)):
#     cars = db.query(Car).all()
#     return {"all": "cars"}


# @app.post("/car", status_code=status.HTTP_201_CREATED)
# def create_post(car: Car):
#     car_dict = car.dict()
#     db.query.append(car_dict)
#     return {"data": car_dict}


# @app.get("/api/v1/cars")
# async def fetch_cars(db: Session = Depends(get_db)):
#     return db.query(Car).all()


# @app.post("/api/v1/cars", status_code=201)
# async def register_cars(car: Car):
#     db.append(car)


# @app.delete("/api/v1/cars/{car_id}", status_code=204)
# async def delete_car(car_id: UUID):
#     for car in db:
#         if car.id == car_id:
#             db.remove(car)
#             return
#         raise HTTPException(
#             status_code=404,
#             detail=f"car with id {car_id} does not exist"
#         )


# @app.put("/api/v1/cars/{car_id}")
# async def update_car(car_update: CarUpdateRequest, car_id: UUID):
#     for car in db:
#         if car.id == car_id:
#             if car_update.car_name is not None:
#                 car.car_name = car_update.car_name
#             if car_update.price is not None:
#                 car.price = car_update.price
#             if car_update.year is not None:
#                 car.year = car_update.year
#             if car_update.car_type is not None:
#                 car.car_type = car_update.car_type
#             if car_update.engine_type is not None:
#                 car.engine_type = car_update.engine_type
#             return
#     raise HTTPException(
#         status_code=404,
#         detail=f"car with id: {car_id} does not exists"
#     )
