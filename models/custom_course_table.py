#!/usr/bin/python3
"""Course Table module"""
from sqlalchemy import Column, String, TEXT, Integer, BLOB
from models import base_model, DB
from sqlalchemy.engine import reflection


db = DB()


def db_exist(class_name):
    """Check table existence"""
    inspector = reflection.Inspector.from_engine(db._DB__engine)
    return inspector.has_table(class_name.lower())


def Course(class_name):
    """Procedure for creating new course table"""
    class_dict = {"__tablename__": str(class_name).lower(),
                  "lesson": Column(String(225), nullable=False, unique=True),
                  'lesson_detail': Column(TEXT, nullable=False),
                  'lesson_number': Column(Integer, nullable=False, unique=True),
                  'lesson_image': Column(TEXT, nullable=True),
                  '__table_args__': {'extend_existing': True}
                  }
    C = type(class_name, ((base_model.BaseModel, base_model.Base, DB)), class_dict)
    C.__table__.create(db._DB__engine, checkfirst=True)
    return C
