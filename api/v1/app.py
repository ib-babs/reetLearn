#!/usr/bin/python3
'''Api main module'''
from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request
from models import db
from os import environ
from flask_jwt_extended import JWTManager
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
app.config['JWT_ALGORITHM'] = 'HS256'
jwt = JWTManager(app)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    db.close()


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
