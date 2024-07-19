#!/usr/bin/python3
"""Quiz Table module"""
from sqlalchemy import Column, TEXT
from models import base_model, DB


def Quiz(class_name):
    """Procedure for creating new quiz table"""
    class_dict = {"__tablename__": str(class_name).lower(),
                  "question": Column(TEXT, nullable=False),
                  "answer": Column(TEXT, nullable=False),
                  "wrong_answer1": Column(TEXT, nullable=False),
                  "wrong_answer2": Column(TEXT, nullable=False),
                    '__table_args__': {'extend_existing': True}
                  }
    db = DB()
    Q = type(class_name, ((base_model.BaseModel, base_model.Base, DB)), class_dict)
    Q.__table__.create(db._DB__engine, checkfirst=True)
    return Q
