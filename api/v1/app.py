#!/usr/bin/python3

from datetime import datetime
from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request
from models import db
from os import environ
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager, decode_token
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    db.close()


@app.get('/check_token')
@jwt_required()
def check_token():
    current_user = get_jwt_identity()
    if current_user:
        token_info = decode_token(request.headers['Authorization'].split()[1])
        exp_time = datetime.fromtimestamp(token_info['exp'])
        current_time = datetime.utcnow()
        if current_time > exp_time:
            return jsonify({"msg": "Token expired"}), 401
        return jsonify({"msg": "Token valid"}), 200
    return jsonify({'msg': "Login required"})


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """ Main Function """
    app.run()
