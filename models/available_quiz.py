#!/usr/bin/python3
'''Class model'''
from sqlalchemy import Column, String, TEXT
from models.base_model import BaseModel, Base
from models import DB

class AvailableQuizes(BaseModel, Base, DB):
    '''Available quizzes modelling'''
    __tablename__ = 'available_quizes'
    quiz_name = Column(String(225), nullable=False, unique=True)
    description = Column(TEXT, nullable=False)
    quiz_image = Column(TEXT, nullable=True)
