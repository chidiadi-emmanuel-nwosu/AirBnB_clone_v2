#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"))
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
