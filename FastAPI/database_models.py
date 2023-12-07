# SQLalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from database import Base


class SQLCar(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    car_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    year = Column(String, nullable=False)
    car_type = Column(ENUM('sedan', 'suv', 'sport',
                      name='car_types'), nullable=False)
    engine_type = Column(
        ENUM('fuel', 'electric', name='engine_types'), nullable=False)
