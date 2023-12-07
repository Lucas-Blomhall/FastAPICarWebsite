# Pydantic,

# är det Schema?
from pydantic import BaseModel
from typing import Optional
# SQLCar class from database_model. SQL = SQLalchemy
# from database_models import SQLCar
from enum import Enum


class Engine_Type(str, Enum):
    fuel = "fuel"
    electric = "electric"


class Car_Type(str, Enum):
    sedan = "sedan"
    suv = "suv"
    sport = "sport"


class PydanticCar(BaseModel):
    id: Optional[int] = None
    car_name: str
    price: int
    year: str
    car_type: Car_Type
    engine_type: Engine_Type

    class Config:
        orm_mode = True


class PydanticCarCreate(BaseModel):
    car_name: str
    price: int
    year: str
    car_type: Car_Type
    engine_type: Engine_Type


class PydanticCarUpdate(BaseModel):
    car_name: Optional[str]
    price: Optional[int]
    year: Optional[str]
    car_type: Optional[Car_Type]
    engine_type: Optional[Engine_Type]
