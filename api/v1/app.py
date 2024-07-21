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
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', '013520634d10aab7f4774e6ba295e43c')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY', '6caad7bb00b457dae71cd097513078e2')
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
