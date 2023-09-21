#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone
"""
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """db storage"""
    __engine = None
    __session = None

    def __init__(self):
        """initialises the engine"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default="localhost")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
                f"mysql+mysqldb://{user}:{pwd}@{host}/{db}", pool_pre_ping=True
                )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """queries the current database"""
        objs_dict = {}

        if not cls:
            objs = [User, State, City, Amenity, Place, Review]

            for obj in objs:
                get_obj = self.__session.query(obj)
                for ob in get_obj:
                    objs_dict[f"{ob.__class__.__name__}.{ob.id}"] = ob
        else:
            if type(cls) == str:
                cls = eval(cls)
            get_obj = self.__session.query(cls)
            for ob in get_obj:
                objs_dict[f"{ob.__class__.__name__}.{ob.id}"] = ob

        return objs_dict

    def new(self, obj):
        """adds an oject to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database"""
        Base.metadata.create_all(self.__engine)

        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """closes all the current database session"""
        self.__session.close()
