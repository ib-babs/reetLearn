#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base
from sqlalchemy.engine import reflection
from os import getenv

def db_exist(class_name, db):
    inspector = reflection.Inspector.from_engine(db)
    if inspector.has_table(class_name.lower()):
        return True
    return False


clss = ['users', "available_courses", "available_quizes"]


class DB:
    __engine = None
    __session = None

    def __init__(self) -> None:
        username = getenv('REETLEARN_MYSQL_USERNAME')
        password = getenv('REETLEARN_MYSQL_PASS')
        host = getenv('REETLEARN_MYSQL_HOST')
        port = getenv('REETLEARN_MYSQL_PORT')
        database_name = getenv('REETLEARN_MYSQL_DB')
        self.__engine = create_engine(
            f"mysql+mysqldb://{username}:{password}@{host}:{port}/{database_name}")

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        if cls and (cls.__tablename__ in clss or
                    db_exist(cls.__name__.lower(), self.__engine)):
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj):
        """delete from the current database session obj if not None"""
        self.__session.delete(obj)

    @classmethod
    def create(cls):
        cls.__table__.create(DB.__engine, checkfirst=False)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine, checkfirst=True)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls and (cls.__tablename__ in clss or
                    db_exist(cls.__name__.lower(), self.__engine)):
            all_cls = models.db.all(cls)

            for value in all_cls.values():
                if (value.id == id):
                    return value
        return None

    def rollback_transaction(self):
        '''Rollback the transaction'''
        self.__session.rollback()

    def drop_all_tables(self):
        '''Drop all tables'''
        Base.metadata.drop_all(self.__engine)

    def drop_table(self, cls):
        cls.__table__.drop(self.__engine)
        return f"{cls.__name__ } table has been dropped!"
