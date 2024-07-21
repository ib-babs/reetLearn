#!/usr/bin/env python3
from io import BytesIO
import json
from pathlib import Path
import shutil
from flask import Flask, render_template, url_for, request, redirect, g, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import db, User
import requests
from PIL import Image
import os
from models.available_courses import AvailableCourses
from models.custom_course_table import Course
from functools import wraps

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.getenv(
    'WEB_FLASK_SECRET_KEY', "bbc021c9a7c47d437e2a6083906cc20753f401ccb524bdaf499cd432b3ca64a0'")
API_URL = os.getenv('API_URL', 'http://localhost:5001/api/v1')


@login_manager.user_loader
def load_user(user_id):
    user = db.get(User, user_id)
    if user:
        g.user_id = user.id
        g.user_info = user.to_dict()
        return user
    return None

def is_token_valid(func):
    '''Checking access token for the api endpoints'''
    @wraps(func)
    def validate_user_token(*args, **kwargs):
        '''Validating token'''
        if current_user.is_authenticated:
            res = requests.get(f'{API_URL}/check_token_status',
                           headers={'Authorization': f'Bearer {session.get("token")}'})
            if res.status_code == 401:
                session.clear()
                g.user_info = None
                g.user_id = None
                logout_user()
                return render_template('expired_token.html')
            if res.status_code == 200:
                return func(*args, **kwargs)
    return validate_user_token



@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('profile', user_id=current_user.id))

    if request.method == 'POST' and 'submit' in request.form:
        form = request.form
        username = form.get('user-name')
        email = form.get('user-email')
        password = form.get('user-password')
        data = json.dumps({
            "username": username, "email":
            (email), "password": (password)
        })
        res = requests.post(f'{API_URL}/register',
                            data=data, headers={"Content-Type": "application/json"})
        g.res_ok = res.status_code
        if res.status_code == 201:
            return redirect(url_for('sign_in'))
        else:
            print(res.json().get('msg'))
            g.sign_up_error = res.json().get('msg')
    return render_template('sign-up.html')


@app.route("/sign-in", methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('profile', user_id=current_user.id))
    if request.method == 'POST' and 'submit' in request.form:
        form = request.form
        email = form.get('email')
        password = form.get('password')
        json_data = json.dumps({
            "email": email, "password": password
        })
        res = requests.post(
            f'{API_URL}/login', json_data, headers={"Content-Type": "application/json"})
        g.res_ok = res.status_code
        print(g.res_ok)
        if res.status_code == 200:
            login_user(db.get(User, res.json().get('user').get('id')))
            session['token'] = res.json().get('access_token')
            return redirect(url_for('profile', user_id=current_user.id))
    return render_template('sign-in.html')


@app.route("/profile/<user_id>", methods=['GET', 'POST'])
@login_required
@is_token_valid
def profile(user_id):
    return render_template('profile.html')


@app.route("/courses", methods=['GET', 'POST'])
@login_required
@is_token_valid
def course_page():
    res = requests.get(f'{API_URL}/available-courses')
    try:
        g.available_courses = res.json()
    except Exception as e:
        pass
    return render_template('courses-page.html')


@app.route("/learn/<course_name>", methods=['GET', 'POST'])
@login_required
@is_token_valid
def lesson_page(course_name):
    g.course = db._DB__session.query(AvailableCourses).filter(
        AvailableCourses.course_name == course_name).first()
    if not g.course:
        return redirect(url_for('course_page'))
    res = requests.get(
        f'{API_URL}/course-table/{course_name}', headers={"Authorization": f"Bearer {session.get('token')}"})
    try:
        g.lessons = res.json()
        g.corse_name = str(course_name).capitalize()
    except Exception as e:
        pass

    return render_template('lesson-page.html')


@app.route('/delete-lesson/<course_name>/<lesson_id>', methods=['GET', 'DELETE'])
@login_required
def delete_lesson(course_name, lesson_id):
    if current_user.role == 'user':
        return redirect(url_for('course_page'))
    res = requests.delete(
        f'{API_URL}//lesson/{course_name}/{lesson_id}',
        headers={"Authorization": f"Bearer {session.get('token')}"})
    if res.status_code != 410:
        g.res_error = res.json().get('msg')
    return redirect(url_for('lesson_page', course_name=course_name))


@app.route("/settings/<user_id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@is_token_valid
def settings(user_id):
    form = request.form
    if request.method == 'POST' and 'submit-profile-btn' in request.form:
        data = {}
        if 'email' in request.form:
            data['email'] = request.form['email']
        if 'username' in request.form:
            data['username'] = request.form['username']
        if 'bio' in request.form and len(request.form['bio']) > 1:
            data['bio'] = request.form['bio']
        if 'country' in request.form:
            data['country'] = request.form['country']
        if 'country-code' in request.form:
            data['country-code'] = request.form['country-code']
        image = request.files.get('uplaod-image')
        if image and image.filename:
            try:
                path = Path(
                    f'{os.getcwd()}/web_flask/static/user-images/{current_user.id}')
                if path.exists():
                    import shutil
                    shutil.rmtree(path)

                path.mkdir(mode=511, exist_ok=True)
                img = Image.open(BytesIO(image.read()))
                img.thumbnail((600, 600))
                img.save(path.joinpath(image.filename))
                data['image'] = f'../static/user-images/{current_user.id}/{image.filename}'
            except Exception as e:
                pass
        res = requests.post(f'{API_URL}/user/{current_user.id}', data=json.dumps(data), headers={
            "Content-Type": "application/json", 'Authorization': f'Bearer {session.get("token")}'})
        # try:
        if res.status_code == 200:
            g.res_ok = True
            g.user_info = res.json().get('user_info')
            return render_template('profile-layout.html', user=g.user_info)
        else:
            g.res_ok = False

    if request.method == 'POST' and 'submit-password-btn' in request.form:
        if 'current-password' in form and 'new-password' in form:
            res = requests.post(f'{API_URL}/user/{current_user.id}',
                                data=json.dumps({'current-password': form.get('current-password'),
                                                'new-password': form.get('new-password')
                                                 }), headers={
                                    "Content-Type": "application/json", 'Authorization': f'Bearer {session.get("token")}'})
            if res.status_code == 200:
                g.res_ok = True
                return render_template('profile-layout.html', user=g.user_info)
            else:
                g.res_ok = False
                g.err = res.json().get('msg')
        return render_template('profile-layout.html', user=current_user)

    if request.method == 'POST' and 'delete-account-btn' in form:
        res = requests.delete(f'{API_URL}/user/{current_user.id}',
                              headers={'Authorization': f"Bearer {session.get('token')}"})
        if res.status_code == 200:
            session.clear()
            logout_user()
            return redirect(url_for('landing_page'))
    return render_template('profile-layout.html', user=current_user)


@app.route('/create-course', methods=['GET', 'POST'])
@login_required
@is_token_valid
def create_course():
    if current_user.role == 'user':
        return redirect(url_for('course_page'))
    form = request.form
    if request.method == 'POST' and 'create-course-submit' in form:
        course_name = form.get('course-name')
        description = form.get('description')
        data = {}
        if course_name:
            data['course-name'] = course_name
        if description:
            data['description'] = description

        if not db._DB__session.query(AvailableCourses).filter(AvailableCourses.course_name == course_name).first():
            image = request.files.get('course-image')
            if image and image.filename:
                try:
                    path = Path(
                        f'{os.getcwd()}/web_flask/static/courses-image/{course_name.replace(" ", "_")}')
                    if path.exists():
                        shutil.rmtree(path)
                        data[
                            'course-image'] = f'../static/courses-image/{course_name.replace(" ", "_")}/{image.filename}'
                    path.mkdir(mode=511, exist_ok=True)
                    img = Image.open(BytesIO(image.read()))
                    img.thumbnail((600, 600))
                    img.save(path.joinpath(image.filename))

                except Exception as e:
                    print(e)
        res = requests.post(f'{API_URL}/new-course',
                            data=json.dumps(data), headers={'Content-Type': 'application/json',
                                                            'Authorization': f'Bearer {session.get("token")}'})
        g.res_status_code = res.status_code
        if res.status_code != 201:
            g.res_error = res.json().get('msg')
    return render_template('create-course.html')


@app.route('/edit-course/<course_name>/<course_id>', methods=['PUT', 'POST', 'GET'])
@login_required
@is_token_valid
def edit_course(course_name, course_id):
    '''Edit a course description and image if available'''
    form = request.form
    if request.method == 'POST' and 'edit-course-submit' in form:
        data = {'description': form.get('description')}
        image = request.files.get('course-image')
        if image and image.filename:
            try:
                    path = Path(
                        f'{os.getcwd()}/web_flask/static/courses-image/{course_name.replace(" ", "_")}')
                    if path.exists():
                        shutil.rmtree(path)
                        data[
                            'course-image'] = f'../static/courses-image/{course_name.replace(" ", "_")}/{image.filename}'
                    path.mkdir(mode=511, exist_ok=True)
                    img = Image.open(BytesIO(image.read()))
                    img.thumbnail((600, 600))
                    img.save(path.joinpath(image.filename))
            except Exception as e:
                    print(e)
        res = requests.put(f'{API_URL}/available-course/{course_id}',
                           data=json.dumps(data), headers={
                               'Content-Type': 'application/json',
                               'Authorization': f'Bearer {session.get("token")}'
                           })
        g.res_status = res.status_code
        if res.status_code != 200:
            g.res_error = res.json().get('msg')
    return redirect(url_for('course_page'))

@app.route('/delete-course/<course_name>', methods=['GET', 'DELETE'])
@login_required
@is_token_valid
def delete_course(course_name):
    """Delete course. This drop the course table from the database"""
    res = requests.delete(f'{API_URL}/delete-course/{course_name}', headers={'Authorization': f'Bearer {session.get("token")}'})
    g.res_status_code = res.status_code
    if res.status_code != 410:
            g.res_error = res.json().get('msg')
    if res.status_code == 410:
        path = Path(f'{os.getcwd()}/web_flask/static/courses-image/{course_name.replace(" ", "_")}')
        if path.exists():
            shutil.rmtree(path)
    return redirect(url_for('course_page'))
    

@app.route('/new-lesson', methods=['GET', 'POST'])
@login_required
@is_token_valid
def add_lesson():
    if current_user.role == 'user':
        return redirect(url_for('course_page'))
    form = request.form
    if request.method == 'POST' and 'add-lesson-submit' in form:
        course_name = form.get('course-name')
        res = requests.post(f'{API_URL}/add-lesson/{course_name}',
                            data=json.dumps(form), headers={'Content-Type': 'application/json',
                                                            'Authorization': f'Bearer {session.get("token")}'})
        g.res_status_code = res.status_code
        if res.status_code != 201:
            g.res_error = res.json().get('msg')
    return render_template('lesson-creation.html')


@app.route("/edit-lesson/<course_name>/<lesson_id>", methods=['GET', 'POST'])
@login_required
@is_token_valid
def edit_lesson(course_name, lesson_id):
    if current_user.role == 'user':
        return redirect(url_for('course_page'))
    g.course_name = course_name
    g.lesson = db.get(Course(course_name), lesson_id)
    if request.method == 'POST' and 'edit-lesson-submit' in request.form:
        form = request.form
        res = requests.put(
            f'{API_URL}//lesson/{course_name}/{lesson_id}',
            data=json.dumps(form), headers={"Authorization": f"Bearer {session.get('token')}",
                                            'Content-Type': 'application/json'})
        g.res_status_code = res.status_code
        if res.status_code != 200:
            g.res_error = res.json().get('msg')
    return redirect(url_for('lesson_page', course_name=course_name))


@app.get('/landing-page')
def landing_page():
    if current_user.is_authenticated:
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('landing_page.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('landing_page'))


@login_manager.unauthorized_handler
def unauthorized_user():
    return redirect(url_for('sign_in'))


if __name__ == '__main__':
    app.run()
