#!/usr/bin/python3
"""Storage engine for databases"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")

classes = {"User": User, "State": State, "City": City,
           "Place": Place, "Review": Review, "Amenity": Amenity}


class DBStorage:
    """
    Database storage representation
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize class instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER,
            HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST,
            HBNB_MYSQL_DB), pool_pre_ping=True)

        env = getenv("HBNB_ENV")
        if (env == "test"):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all instances of given class name"""

        instances = {}
        if cls:
            for row in self.__session.query(cls).all():
                key = ("{}.{}".format(cls.__name__, row.id))
                row.to_dict()
                instances[key] = row
        else:
            for bnb_class in classes.values():
                rows = self.__session.query(bnb_class).all()
                for row in rows:
                    key = ("{}.{}".format(row.__class__.__name__, row.id))
                    row.to_dict()
                    instances[key] = row
        return instances

    def new(self, obj):
        """add obj to current session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commmit all changes to current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in DB"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Scope = scoped_session(Session)
        self.__session = Scope()
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()"""

    def close(self):
        """Close current session"""
        self.__session.close()
