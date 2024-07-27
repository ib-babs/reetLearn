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
    json = request.get_json()
    if not json:
        return jsonify({'msg': 'Not a JSON'}), 400
    quiz_name = json.get('quiz_name')
    description = json.get('description')
    quiz_image = json.get('quiz_image')
    if not quiz_image:
        quiz_image = '../static/images/logo.png'
    if not quiz_name or not description:
        return jsonify({"msg": "'quiz_name' and 'description' required"}), 400
    if not quiz_name.endswith("Quiz"):
        return jsonify({"msg": "quiz_name should ends with `Quiz`"}), 400
    underscore_quiz = str(quiz_name).replace(' ', '_')

    if not db_exist(underscore_quiz):
        Quiz(underscore_quiz)
        available_quiz = AvailableQuizes(quiz_name=str(quiz_name).strip(),
                                         description=str(description).capitalize().strip(),
                                         quiz_image=quiz_image)
        try:
            db.new(available_quiz)
            db.save()
        except Exception as e:
            print(e)
            db.rollback_transaction()
            pass
        return make_response(jsonify({'msg': f"{quiz_name} table is created!"})), 201

    return jsonify({"msg": f"{quiz_name} is already exit!"}), 403


@app_views.get('/quiz-table/<quiz_name>', strict_slashes=False)
@jwt_required()
def get_all_quiz(quiz_name):
    """Create new quiz table"""
    if not db_exist(quiz_name.replace(' ', '_')):
        return jsonify({"msg": "No quiz table with such name exist!"}), 404
    MyQuiz = Quiz(quiz_name.replace(' ', '_'))
    q = db._DB__session.query(MyQuiz).order_by(MyQuiz.question_number).distinct(MyQuiz.question).all()
    all_quizzes = [quiz.to_dict() for quiz in q]
    concepts = set()
    if all_quizzes:
        concepts = set([concept.get('concept') for concept in all_quizzes])
    
    return jsonify({'quizzes': all_quizzes, 'concepts': list(concepts)}), 200


@app_views.post('/quiz/<quiz_name>', strict_slashes=False)
@jwt_required()
def add_quiz(quiz_name):
    underscore_quiz = str(quiz_name).replace(' ', '_')
    if not db_exist(underscore_quiz):
        return jsonify({"msg": "No quiz with such name!"}), 404
    data = request.get_json()
    if not data:
        jsonify(msg="Not a JSON"), 400
    concept = data.get('concept')
    question = data.get('question')
    answer = data.get('answer')
    wrong_answer1 = data.get('wrong_answer1')
    wrong_answer2 = data.get('wrong_answer2')
    question_number = data.get('question_number')
    if not question or not answer or \
            not wrong_answer1 or not wrong_answer2 or not question_number or not concept:
        return jsonify({"Usage": "Require `concept`, `quiz_name`\
                       `answer` `wrong_answer1`, `question_number` and `wrong_answer2` "}), 400
    new_quiz = Quiz(underscore_quiz)(**data)
    try:
        db.new(new_quiz)
        db.save()
    except Exception as e:
        print(e)
        db.rollback_transaction()
        return jsonify({"msg": '`concept` field must be unique!'}), 400
    return jsonify({"msg": f"New quiz is added to {quiz_name.capitalize()}"}), 201


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
            return jsonify({"msg": '`lesson` and `lesson_number` fields must be unique!'}), 403
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
        return jsonify({"msg": "Error encountered"}), 500
    return jsonify({"msg": f"{quiz_name.capitalize()}.{quiz_id} has been deleted!"})


@app_views.delete('/delete-quiz/<quiz_name>', strict_slashes=False)
@jwt_required()
def drop_quiz(quiz_name):
    if not db_exist(quiz_name.replace(" ", "_")):
        return jsonify({"msg": "No quiz with such name!"}), 404
    available_quiz = db._DB__session.query(AvailableQuizes).\
        filter(AvailableQuizes.quiz_name == quiz_name.capitalize()).first()
    MyQuiz = Quiz(quiz_name.replace(' ', '_'))
    try:
        db.drop_table(MyQuiz)
        db.delete(available_quiz)
        db.save()
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error encountered"}), 500
    return jsonify({"msg": f"{quiz_name} has been successfully deleted!"}), 410
