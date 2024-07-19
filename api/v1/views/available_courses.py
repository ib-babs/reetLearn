#!/usr/bin/python3
from datetime import datetime
from models import db, AvailableCourses
from api.v1.views import app_views, check_user_role
from flask import jsonify, request, abort, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.get('/available-courses', strict_slashes=False)
def get_all_available_courses():
    all_quizes = [quiz.to_dict() for quiz in db.all(AvailableCourses).values()]
    return jsonify(all_quizes)


@app_views.get('/available-course/<available_course_id>', strict_slashes=False)
def get_course_available(available_course_id):
    '''Get available_course by id'''
    available_course = db.get(AvailableCourses, available_course_id)
    if available_course:
        return jsonify(available_course.to_dict())
    return jsonify({})


@app_views.put('/available-course/<available_course_id>', strict_slashes=False)
@jwt_required()
def edit_available_course(available_course_id):
    check_user_role(get_jwt_identity().get('role'))
    if not request.get_json():
        return jsonify({'msg': 'Not a JSON'}), 400
    available_course = db.get(AvailableCourses, available_course_id)
    if not available_course:
        return jsonify(msg="Unavailable"), 404
    description = request.get_json().get('description')
    course_image = request.get_json().get('course-image')

    if description or course_image:
        if description:
            available_course.description = description
        if course_image:
            available_course.course_image = course_image
        available_course.updated_at = datetime.now()
        try:
            db.save()
        except Exception as e:
            db.rollback_transaction()
        return make_response(jsonify({'message':
                                      f"AvailableCourses.{available_course_id} has been updated"}))
    return jsonify(msg="No available_courses data field found"), 400
