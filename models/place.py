#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import models
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")

if (storage_type == "db"):
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=False,
                                 nullable=False)
                          )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """return reviews"""
            review_list = models.storage.all(models.review.Review)
            res = []
            for rev in review_list.values():
                if rev.place_id == self.id:
                    res.append(rev)
            return res

        @property
        def amenities(self):
            """return amenities"""
            amenities_list = models.storage.all(models.amenity.Amenity)
            res = []
            for ame in amenities_list.values():
                if ame.id in self.amenity_ids:
                    res.append(ame)
            return res

        @amenities.setter
        def amenities(self, obj):
            """Settter prop for amenities"""
            if obj is not None:
                if isinstance(obj, models.amanity.Amenity):
                    if obj.id not in self.amenity_ids:
                        self.amenity_ids.append(obj.id)
