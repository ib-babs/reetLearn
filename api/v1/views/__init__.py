#!/usr/bin/python3
"""__init__.py"""
# from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

def check_user_role(role):
    if role == "admin":
        return True
    return False
from api.v1.views.user import *
from api.v1.views.course_creation import *
from api.v1.views.quiz_creation import *
from api.v1.views.available_courses import *
from api.v1.views.available_quizes import *
from api.v1.views.index import *