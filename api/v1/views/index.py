#!/usr/bin/python3
"""index.py"""
from api.v1.views import app_views, jsonify
@app_views.get('/', strict_slashes=False)
def index():
    '''All api endpoint'''
    endpoints=[
        'GET /api/v1/users',
        'POST /api/v1/user',
        'DELETE /api/v1/user',
        'PUT /api/v1/user',
    ]
    return jsonify(index=endpoints)

