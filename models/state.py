#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from os import getenv
from datetime import datetime


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref="state", cascade="all, delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """returns a list of cities"""
            from models import storage

            city_list = []

            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)

            return city_list
