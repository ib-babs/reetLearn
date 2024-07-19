from flask import jsonify, Blueprint

blueprint = Blueprint('api', __name__, url_prefix="/api/v1")
courses = [{'id': 1, "course_title": "Python", "course": [{
    "Variable": "Variable is a placeholder pointing to the memory location of data defined",
    "String": "String is the combination of characters"
}]}, {"id": 2, "course_name": "JavaScript", "course": [{
    "Variable Declaration": "Variables can be declared with my keywords e.g const, let, var",
    "String": "String is the combination of characters"}]}]


@blueprint.get("/")
def get_all_courses():
    return jsonify([course for course in courses])


@blueprint.post("/add-course")
def add_course():
    courses.append({'id': 3, "course_title": "Python", "course": [{
        "Variable": "Variable is a placeholder pointing to the memory location of data defined",
        "String": "String is the combination of characters"
    }]})
    return jsonify([course for course in courses])


@blueprint.get("/course/<int:id>")
def get_course(id):
    res = [course for course in courses if id == course.get('id')]
    return jsonify({"message": "No course found"} if not res else res[0])
