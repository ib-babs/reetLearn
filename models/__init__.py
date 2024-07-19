#!/usr/bin/python3
"""__init__.py"""
from models.engine.db import DB
from models.custom_course_table import Course
from models.custom_quiz_table import Quiz
from models.user import User
from models.available_courses import AvailableCourses
from models.available_quiz import AvailableQuizes

custom_course_table = Course
custom_quiz_table = Quiz

db = DB()
db.reload()
