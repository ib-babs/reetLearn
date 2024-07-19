#!/usr/bin/python3
from datetime import datetime
from models import db, AvailableQuizes
from api.v1.views import app_views
from flask import jsonify, request, make_response

 
@app_views.get('/available-quizes', strict_slashes=False)
def get_all_available_quizes():
    all_available_quizes = [quiz.to_dict()
                            for quiz in db.all(AvailableQuizes).values()]
    return jsonify(all_available_quizes)


@app_views.get('/available-quiz/<available_quiz_id>', strict_slashes=False)
def get_available_quiz(available_quiz_id):
    '''Get available_quiz by id'''
    available_quiz = db.get(AvailableQuizes, available_quiz_id)
    if available_quiz:
        return jsonify(available_quiz.to_dict())
    return jsonify({})


@app_views.put('/available-quiz/<available_quiz_id>', strict_slashes=False)
def edit_available_quiz(available_quiz_id):
    available_quiz = db.get(AvailableQuizes, available_quiz_id)
    if not available_quiz:
        return jsonify(msg="Unavailable"), 404
    if not request.get_json():
        return jsonify(msg="Not a JSON"), 400
    description = request.get_json().get('description')
    quiz_image = request.get_json().get('quiz_image')

    if description or quiz_image:
        if description:
            available_quiz.description = description
        if quiz_image:
            available_quiz.quiz_image = quiz_image
        available_quiz.updated_at = datetime.now()

        try:
            db.save()
        except Exception as e:
            db.rollback_transaction()
        return make_response(jsonify({'message':
                                      f"AvailableQuizes.{available_quiz_id} has been updated"}))
    return jsonify(msg="No available_quizes data field found"), 400
