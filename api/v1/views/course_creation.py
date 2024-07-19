#!/usr/bin/python3

from datetime import datetime
from models import Course, db, AvailableCourses
from api.v1.views import app_views, check_user_role
from flask import jsonify, request, abort, make_response
from models.custom_course_table import db_exist, reflection
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.get('/all_tables', strict_slashes=False)
@jwt_required()
def all_tables():
    check_user_role(get_jwt_identity().get('role'))
    inspector = reflection.Inspector.from_engine(db._DB__engine)
    return jsonify(inspector.get_table_names())


@app_views.post('/new-course', strict_slashes=False)
@jwt_required()
def create_course_table():
    """Create new course table"""
    data = request.get_json()
    course_name = data.get('course-name')
    description = data.get('description')
    course_image = data.get('course-image')

    if not course_name or not description:
        return jsonify({"msg": "`course-name` and `description` required"}), 400
    underscore_course = str(course_name).replace(' ', '_')
    if not db_exist(underscore_course):
        if not course_image:
            course_image = '../static/images/logo.png'
        Course(underscore_course)
        available_course = AvailableCourses(course_name=str(course_name).strip(),
                                            description=str(description).strip(),
                                            course_image=course_image.replace(' ', "_"))
        try:
            db.new(available_course)
            db.save()
        except Exception  as e:
            print(e)
            db.rollback_transaction()
        return make_response(jsonify({'msg': f"{course_name} table is created!"})), 201
    else:
        print(course_image)
        return jsonify({"msg": f"{course_name} table is already exit!"}), 403


@app_views.get('/course-table/<course_name>', strict_slashes=False)
@jwt_required()
def get_all_lesson(course_name):
    """Get lessons"""
    if not db_exist(course_name):
        return jsonify({"msg": "No course table with such name exist!"}), 404
    MyCourse = Course(course_name)
    sorted_lessons = []
    all_lessons = [lesson.to_dict() for lesson in db.all(MyCourse).values()]
    if all_lessons:
        sorted_lessons = sorted(
                [lesson for lesson in all_lessons], key=lambda x: x.get('lesson_number'))
    return jsonify(sorted_lessons)


@app_views.post('/add-lesson/<course_name>', strict_slashes=False)
@jwt_required()
def add_lesson(course_name):
    if not db_exist(course_name):
        return jsonify({"msg": "No course with such name!"}), 404
    data = request.get_json()
    if not data:
        return jsonify(msg="Not a JSON"), 400
    lesson = data.get('lesson')
    lesson_detail = data.get('lesson_detail').replace('\n', '<br/>')
    lesson_number = data.get('lesson_number')
    if not lesson or \
            not lesson_detail or not lesson_number:
        return jsonify({"Usage": "Require `course_name`\
                        `lesson` `lesson_detail` and `lesson_number` "}), 400
    new_course = Course(course_name)(**data)
    try:
        db.new(new_course)
        db.save()
    except Exception as e:
        db.rollback_transaction()
        return jsonify({"msg": '`lesson` and `lesson_number` fields must be unique!'})
    return jsonify({"msg": f"New lesson added to {course_name.capitalize()}"}), 201


@app_views.put('/lesson/<course_name>/<lesson_id>', strict_slashes=False)
@jwt_required()
def edit_lesson(course_name, lesson_id):
    if not db_exist(course_name):
        return jsonify({"msg": "No Course with such name!"}), 404
    data = request.get_json()
    if not data:
        jsonify({"msg": "Not a JSON"}), 400
    lesson_obj = db.get(Course(course_name), lesson_id)
    lesson = data.get('lesson')
    lesson_detail = data.get('lesson_detail')
    lesson_number = data.get('lesson_number')

    if lesson or lesson_detail or lesson_number:
        if lesson:
            lesson_obj.lesson = lesson
        if lesson_detail:
            lesson_obj.lesson_detail = lesson_detail
        if lesson_number:
            lesson_obj.lesson_number = lesson_number
        lesson_obj.updated_at = datetime.now()
        try:
            db.save()
        except Exception as e:
            db.rollback_transaction()
            return jsonify({"msg": '`lesson` and `lesson_number` fields must be unique!'}), 400
        return jsonify({'msg': f"Changes has been made to {course_name}.{lesson_id}"}), 200

    return jsonify(msg="No lesson data field found"), 400


@app_views.delete('/lesson/<course_name>/<lesson_id>', strict_slashes=False)
@jwt_required()
def delete_lesson(course_name, lesson_id):
    if not db_exist(course_name):
        return jsonify({"msg": "No Course with such name!"}), 404
    lesson = db.get(Course(course_name), lesson_id)
    if not lesson:
        return jsonify(msg="No lesson found"), 404
    try:
        db.delete(lesson)
        db.save()
    except Exception as e:
        return jsonify({"msg": "Error encountered"}), 500
    return jsonify({"msg": f"{course_name}.{lesson.id} has been deleted!"}), 410


@app_views.delete('/drop-course-table/<table_name>', strict_slashes=False)
@jwt_required()
def drop(table_name):
    check_user_role(get_jwt_identity().get('role'))
    if not db_exist(table_name):
        return jsonify({"msg": "No table with such name!"}), 404
    available_course = db._DB__session.query(AvailableCourses).\
        filter(AvailableCourses.course_name == table_name.capitalize()).first()
    MyCourse = Course(table_name)
    try:
        db.drop_table(MyCourse)
        db.delete(available_course)
        db.save()
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error encountered"}), 500
    return jsonify({"msg": f"{table_name} has been dropped!"}), 404
