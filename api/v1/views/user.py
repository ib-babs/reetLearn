#!/usr/bin/python3
from datetime import datetime, timedelta
from models import db
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required, decode_token
import bcrypt


@app_views.post('/register', strict_slashes=False)
def register():
    data = request.get_json()
    if not data:
        jsonify({"msg": "Not a JSON"}), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({"msg": "Missing username or email or password"}), 400
    new_user = User(**data)
    try:
        db.new(new_user)
        db.save()
    except Exception as e:
        db.rollback_transaction()
        return jsonify({"msg": "User with this email exist!"}), 409
    return jsonify({'msg': "New user is created"}), 201


@app_views.post('/login', strict_slashes=False)
def login():
    '''Log user in'''
    data = request.get_json()
    if not data:
        jsonify({"msg": "Not a JSON"}), 400
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400
    user = db._DB__session.query(User).\
        filter(User.email == email).first()

    if user and bcrypt.checkpw(str(password).encode(), user.password.encode()):
        access_token = create_access_token(
            identity=user.to_dict(), expires_delta=timedelta(days=5))
        return jsonify({"access_token": access_token, 'user': user.to_dict()}), 200
    return jsonify({"msg": "Email or password is incorrect!"}), 404


@app_views.get('/user/<user_id>', strict_slashes=False)
@jwt_required()
def get_user(user_id):
    '''Get user by id'''
    user = db.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"msg": "User doesn't exist!"})


@app_views.get('/users', strict_slashes=False)
@jwt_required()
def get_users():
    all_users = [user.to_dict() for user in db.all(User).values()]
    return jsonify(all_users)


@app_views.post('/user/<user_id>', strict_slashes=False)
@jwt_required()
def edit_user(user_id):
    data = request.get_json()
    user = db.get(User, user_id)
    if not user:
        return jsonify(msg="No user found"), 404
    if not data:
        jsonify({"msg": "Not a JSON"}), 400
    username = data.get('username')
    email = data.get('email')
    current_password = data.get('current-password')
    new_password = data.get('new-password')
    country = data.get('country')
    image = data.get('image')
    bio = data.get('bio')
    country_code = data.get('country-code')

    if username or email or current_password \
            or new_password or country or image or country_code:
        if username and len(username) > 1 and user.username != username:
            user.username = username
        if email and user.email != email:
            user.email = email
        if current_password and new_password:
            if bcrypt.checkpw(str(current_password).encode(), str(user.password).encode())\
                and len(str(new_password)) > 5:
                user.password = new_password
            else:
                return jsonify({'msg': "Current password is incorrect!"}), 400
        if country and country != user.country:
            user.country = country
        if country_code and country_code != user.country_code:
            user.country_code = country_code
        if image:
            user.image = image
        if bio and len(bio) > 2 and user.bio != bio:
            user.bio = bio
        user.updated_at = datetime.now()

        try:
            db.save()
        except Exception as e:
            db.rollback_transaction()
            return jsonify({"msg": "User with this email already exist!"}), 500
        return jsonify({'msg': f"Changes has been made to User.{user_id}",  'user_info': user.to_dict()}), 200
    return jsonify(msg="No user data field found"), 400


@app_views.delete('/user/<user_id>', strict_slashes=False)
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    if current_user.get("id") != user_id:
        return jsonify({"msg": "Unauthorized"}), 403
    user = db.get(User, user_id)
    if not user:
        return jsonify(msg="No user found"), 404
    db.delete(user)
    db.save()
    return jsonify({"msg": f"User.{user_id} deleted successfully!"}), 200
