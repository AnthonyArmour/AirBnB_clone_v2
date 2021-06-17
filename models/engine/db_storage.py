#!/usr/bin/python3
"""Contains db_storage"""
from models.review import Review
from models.place import Place
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from sqlalchemy import create_engine
from os import environ


class DBStorage():
    """DBStorage class"""
    class_dic = {'State': State,
                 'City': City,
                 'User': User,
                 'Place': Place,
                 'Review': Review,
                 'Amenity': Amenity}

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(environ.get('HBNB_MYSQL_USER'),
                                              environ.get('HBNB_MYSQL_PWD'),
                                              environ.get('HBNB_MYSQL_HOST'),
                                              environ.get('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """All method queries databasse for all objects"""
        dic = {}
        objects = []
        if cls is not None:
            objects.extend(self.__session.query(
                           self.class_dic[cls.__name__]).all())
        else:
            for clss in self.class_dic.values():
                objects.extend(self.__session.query(clss).all())
        for item in objects:
            st = type(item).__name__ + '.' + item.id
            dic.update({st: item})
        return dic

    def new(self, obj):
        """Adds object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Saves current database session"""
        self.__session.commit()

    def delete(self, obj):
        """Deletes and object from current database session"""
        self.__session.delete(obj)

    def close(self):
        """closes session"""
        self.__session.remove()
        self.reload()

    def reload(self):
        """Creates all tables in database"""
        from sqlalchemy.orm import sessionmaker, scoped_session
        from sqlalchemy.orm.session import Session

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
