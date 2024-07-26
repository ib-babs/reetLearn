#!/usr/bin/python3
from sqlalchemy import Column,  String, TEXT, VARCHAR
from bcrypt import hashpw, gensalt
from models.base_model import BaseModel, Base
from models import DB
# from web_flask.app import app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



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
    def get_reset_token(self, app, expire_sec=1800):
            '''Get the reset token. Expires in thirty minutes'''
            s = Serializer(app.config['SECRET_KEY'], expires_in=expire_sec)
            return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(db, cls, app, token):
            '''Verifying token'''
            s = Serializer(app.config['SECRET_KEY'])
            try:
                user_id = s.loads(token)['user_id']
            except:
                return None
            return db.get(cls, user_id)
