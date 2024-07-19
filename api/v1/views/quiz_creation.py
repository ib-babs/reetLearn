#!/usr/bin/python3

from datetime import datetime
from models import Quiz, db, AvailableQuizes
from api.v1.views import app_views, check_user_role
from flask import jsonify, request, make_response
from models.custom_course_table import db_exist
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.post('/new-quiz', strict_slashes=False)
@jwt_required()
def create_quiz_table():
    """Create new quiz table"""
    check_user_role(get_jwt_identity().get('role'))
    quiz_name = request.form.get('quiz_name')
    description = request.form.get('description')

    if not quiz_name or not description:
        return jsonify({"msg": "`quiz_name` and `description` required"}), 400
    if not quiz_name.endswith("quiz"):
        return jsonify({"error": "quiz_name should ends with `quiz`"})
    if not db_exist(quiz_name):
        Quiz(quiz_name)
        available_quiz = AvailableQuizes(quiz_name=str(quiz_name).capitalize(),
                                         description=str(description).capitalize())
        try:
            db.new(available_quiz)
            db.save()
        except Exception as e:
            print(e)
            db.rollback_transaction()
            pass
        return make_response(jsonify({'msg': f"{quiz_name} table is created!"})), 201

    return jsonify({"error": f"{quiz_name} table is already exit!"}), 403


@app_views.get('/quiz-table/<quiz_name>', strict_slashes=False)
@jwt_required()
def get_all_quiz(quiz_name):
    """Create new quiz table"""
    if not db_exist(quiz_name):
        return jsonify({"error": "No quiz table with such name exist!"}), 404
    MyQuiz = Quiz(quiz_name)

    all_quizes = [quiz.to_dict() for quiz in db.all(MyQuiz).values()]
    return jsonify(all_quizes)


@app_views.post('/quiz/<quiz_name>', strict_slashes=False)
@jwt_required()
def add_quiz(quiz_name):
    check_user_role(get_jwt_identity().get('role'))
    if not db_exist(quiz_name):
        return jsonify({"msg": "No quiz with such name!"}), 404
    data = request.get_json()
    if not data:
        jsonify(msg="Not a JSON"), 400
    question = data.get('question')
    answer = data.get('answer')
    wrong_answer1 = data.get('wrong_answer1')
    wrong_answer2 = data.get('wrong_answer2')
    if not question or not answer or \
            not wrong_answer1 or not wrong_answer2:
        return jsonify({"Usage": "Require `quiz_name`\
                        answer` `wrong_answer1` and `wrong_answer2` "}), 400
    new_quiz = Quiz(quiz_name)(**data)
    try:
        db.new(new_quiz)
        db.save()
    except Exception as e:
        print(e)
        db.rollback_transaction()
        return jsonify({"error": '`lesson` and `lesson_number` fields must be unique!'})
    return jsonify({"msg": f"New quiz is added to {quiz_name.capitalize()}"})


@app_views.put('/quiz/<quiz_name>/<quiz_id>', strict_slashes=False)
@jwt_required()
def edit_quiz(quiz_name, quiz_id):
    check_user_role(get_jwt_identity().get('role'))
    if not db_exist(quiz_name):
        return jsonify({"msg": "No quiz with such name!"}), 404

    data = request.get_json()
    if not data:
        jsonify({"msg": "Not a JSON"}), 400
    question = data.get('question')
    answer = data.get('answer')
    wrong_answer1 = data.get('wrong_answer1')
    wrong_answer2 = data.get('wrong_answer2')

    quiz_obj = Quiz(quiz_name)
    if question or answer or wrong_answer1 or wrong_answer2:
        if question:
            quiz_obj.question = question
        if answer:
            quiz_obj.answer = answer
        if wrong_answer1:
            quiz_obj.wrong_answer1 = wrong_answer1
        if wrong_answer2:
            quiz_obj.wrong_answer2 = wrong_answer2
        quiz_obj.updated_at = datetime.now()

        try:
            db.save()
        except Exception as e:
            db.rollback_transaction()
            return jsonify({"error": '`lesson` and `lesson_number` fields must be unique!'}), 403
        return jsonify({'msg': f"Changes has been made to {quiz_name}.{quiz_id}"})

    return jsonify(msg="No quiz data field found"), 400


@app_views.delete('/quiz/<quiz_name>/<quiz_id>', strict_slashes=False)
@jwt_required()
def delete_quiz(quiz_name, quiz_id):
    check_user_role(get_jwt_identity().get('role'))
    if not db_exist(quiz_name):
        return jsonify({"msg": "No quiz with such name!"}), 404
    quiz = db.get(Quiz(quiz_name), quiz_id)
    if not quiz:
        jsonify(msg="No quiz found"), 400
    try:
        db.delete(quiz)
        db.save()
    except Exception as e:
        return jsonify({"error": "Error encountered"}), 500
    return jsonify({"msg": f"{quiz_name.capitalize()}.{quiz_id} has been deleted!"})


@app_views.delete('/drop-quiz-table/<table_name>', strict_slashes=False)
@jwt_required()
def drop_quiz(table_name):
    check_user_role(get_jwt_identity().get('role'))
    if not db_exist(table_name):
        return jsonify({"msg": "No table with such name!"}), 404
    available_quiz = db._DB__session.query(AvailableQuizes).\
        filter(AvailableQuizes.quiz_name == table_name.capitalize()).first()
    MyQuiz = Quiz(table_name)
    try:
        db.drop_table(MyQuiz)
        db.delete(available_quiz)
        db.save()
    except Exception as e:
        print(e)
        return jsonify({"error": "Error encountered"}), 500
    return jsonify({"msg": f"{table_name} has been dropped!"}), 404
