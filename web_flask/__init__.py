#!/usr/bin/env python3
import json
import bcrypt
import requests
from models.available_courses import AvailableCourses
from models.available_quiz import AvailableQuizes
from models.custom_course_table import Course
from functools import wraps
from flask import Flask, url_for, render_template, request, redirect, g, session
import base64
from io import BytesIO
from os import environ
from PIL import Image
from models import db, User
from flask_mail import Mail, Message
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
API_URL = environ.get('API_URL', 'http://localhost:5001/api/v1')


def save_image_to_db(image_file=None):
    '''Resize image before saving it to the database'''
    img = Image.open(BytesIO(image_file.read()))
    img.thumbnail((300, 300))
    image_fmt = img.format.lower()
    buffered = BytesIO()
    img.save(buffered, format=f'{image_fmt}')
    return (base64.b64encode(buffered.getvalue()).decode('utf-8'), image_fmt)


def is_token_valid(func):
    '''Checking access token for the api endpoints'''
    @wraps(func)
    def validate_user_token(*args, **kwargs):
        '''Validating token'''
        if current_user.is_authenticated:
            res = requests.get(f'{API_URL}/check_token_status',
                               headers={'Authorization': f'Bearer {session.get("token")}'})
            if res.status_code != 200:
                session.clear()
                g.user_info = None
                g.user_id = None
                logout_user()
                return render_template('expired_token.html')
            if res.status_code == 200:
                return func(*args, **kwargs)
    return validate_user_token
