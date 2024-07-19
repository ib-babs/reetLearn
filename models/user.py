#!/usr/bin/python3
from sqlalchemy import Column,  String, TEXT, VARCHAR
from bcrypt import hashpw, gensalt
from models.base_model import BaseModel, Base
from models import DB
from flask_login import UserMixin


class User(BaseModel, Base, DB, UserMixin):
    __tablename__ = 'users'
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    country = Column(String(128), nullable=False, default="Nigeria")
    role = Column(String(128), nullable=False, default='user')
    image = Column(TEXT, nullable=True)
    bio = Column(TEXT, nullable=True)
    country_code = Column(String(3), default='ng', nullable=True)
    oauth_provider = Column(String(60), nullable=True)
    oauth_id = Column(String(60), nullable=True)
    # user_progess = relationship(
    #     'UserProgress', backref='user_progress', cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = hashpw(str(value).encode(), gensalt())
        super().__setattr__(name, value)
