#!/usr/bin/python3
"""index.py"""
from api.v1.views import app_views, jsonify


@app_views.get('/', strict_slashes=False)
def index():
    '''All api endpoint'''
    endpoints = [
        'GET /api/v1/check_token_status',
        'POST /api/v1/register',
        'POST /api/v1/login',
        'GET /api/v1/users',
        'PUT /api/v1/user/<user_id>',
        'DELETE /api/v1/user/<user_id>',
        'PUT /api/v1/user',
        'GET /api/v1/available-courses',
        'GET /api/v1/available-course/<available_course_id>',
        'PUT /api/v1/available-course/<available_course_id>',
        'GET /api/v1/available-quizes',
        'GET /api/v1/available-quiz/<available_quiz_id>',
        'PUT /api/v1/available-quiz/<available_quiz_id>',
        'GET /api/v1/all_tables',
        'POST /api/v1/new-course',
        'GET /api/v1/course-table/<course_name>',
        'POST /api/v1/add-lesson/<course_name>',
        'PUT /api/v1/lesson/<course_name>/<lesson_id>'
        'DELETE /api/v1/lesson/<course_name>/<lesson_id>',
        'DELETE /api/v1/delete-course/<course_name>',
        'POST /api/v1/new-quiz',
        'GET /api/v1/quiz-table/<quiz_name>',
        'POST /api/v1/quiz/<quiz_name>',
        'PUT /api/v1/quiz/<quiz_name>/<quiz_id>',
        'DELETE /api/v1/quiz/<quiz_name>/<quiz_id>',
        'DELETE /api/v1/delete-quiz/<quiz_name>'
    ]
    return jsonify(endpoints=endpoints), 200
