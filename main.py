from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from pydantic_models import PydanticCar
from database_models import SQLCar

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cars", response_model=list[PydanticCar])
def read_cars(db: Session = Depends(get_db)):
    cars = db.query(SQLCar).all()
    return cars


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
