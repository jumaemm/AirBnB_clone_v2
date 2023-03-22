#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if (storage_type == 'db'):
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ""

        @property
        def cities(self):
            """Getter method for all cities"""
            list_cities = models.storage.all(models.city.City).values()
            res = []
            for city in list_cities:
                if (city.state_id == self.id):
                    res.append(city)
            return res
