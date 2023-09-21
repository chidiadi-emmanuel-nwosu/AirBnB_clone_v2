#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table, DateTime
from sqlalchemy.orm import relationship
from os import getenv
from datetime import datetime


place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True
            ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True
            )
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
                "Review", backref="place", cascade="all, delete"
                )
        amenities = relationship(
                "Amenity", secondary=place_amenity, viewonly=False
                )
    else:
        @property
        def reviews(self):
            """returns the list of Review instances"""
            review_list = []

            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)

            return review_list

        @property
        def amenities(self):
            """returns the list of Amenity instances based on amenity_ids"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """andles append method for adding an Amenity.id
               to the attribute amenity_ids
            """
            if type(obj) == Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
