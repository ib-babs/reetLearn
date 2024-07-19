#!/usr/bin/python3
from sqlalchemy import Column, String, TEXT
from models.base_model import BaseModel, Base
from models import DB

class AvailableCourses(BaseModel, Base, DB):
    __tablename__ = 'available_courses'
    course_name = Column(String(225), nullable=False, unique=True)
    description = Column(TEXT, nullable=False)
    course_image = Column(TEXT, nullable=True)
