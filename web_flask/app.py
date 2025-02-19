#!/usr/bin/env python3
'''app.py'''
from datetime import timedelta
from web_flask import *

app = Flask(__name__)
def send_reset_email(user):
    '''Send reset email message'''
    token = user.get_reset_token(app)
    msg = Message('Password Reset Request', sender=environ.get('EMAIL_USER'), recipients=[
                  user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
Ignore the message if you don't request for password reset and no change will be made!'''
    mail.send(msg)
    return 'Email is sent successfully!'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True  # or False for SSL
app.config['MAIL_USERNAME'] = environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = environ.get('EMAIL_PASS')
app.config['SECRET_KEY'] = environ.get('WEB_FLASK_SECRET_KEY')
login_manager = LoginManager(app)
login_manager.init_app(app)

# Mail Manager
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    '''load users'''
    user = db.get(User, user_id)
    if user:
        g.user_id = user.id
        g.user_info = user.to_dict()
        return user
    return None


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    '''Register user'''
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
        g.res_status_code = res.status_code
        if res.status_code == 201:
            return redirect(url_for('sign_in'))
        else:
            g.res_error = res.json().get('msg')
    return render_template('sign-up.html')


@app.route("/sign-in", methods=['GET', 'POST'])
def sign_in():
    '''Login user with correct credential'''
    if current_user.is_authenticated:
        return redirect(url_for('profile', user_id=current_user.id))
    if request.method == 'POST' and 'submit' in request.form:
        form = request.form
        email = form.get('email')
        password = form.get('password')
        json_data = json.dumps({
            "email": email, "password": password
        })

        try:
            res = requests.post(
                f'{API_URL}/login', json_data, headers={"Content-Type": "application/json"})
            g.res_status = res.status_code
            if res.status_code == 200:
                id = res.json().get('user').get('id')
                login_user(db.get(User, id), remember=True, duration=timedelta(days=7))
                session['token'] = res.json().get('access_token')
                return redirect(url_for('profile', user_id=current_user.id))
            else:
                g.res_error = res.json().get('msg')
        except Exception as e:
            pass
    return render_template('sign-in.html')


@app.route("/profile/<user_id>", methods=['GET', 'POST'])
@login_required
@is_token_valid
def profile(user_id):
    """User's profile"""
    return render_template('profile.html')


@app.route("/settings/<user_id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@is_token_valid
def settings(user_id):
    '''Settings'''
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
                data['image'] = save_image_to_db(image_file=image)[0]
            except Exception as e:
                pass
        res = requests.post(f'{API_URL}/user/{current_user.id}', data=json.dumps(data), headers={
            "Content-Type": "application/json", 'Authorization': f'Bearer {session.get("token")}'})
        # try:
        g.res_status_code = res.status_code
        if res.status_code == 200:
            g.user_info = res.json().get('user_info')
            return render_template('profile-layout.html', user=g.user_info)

    if request.method == 'POST' and 'submit-password-btn' in request.form:
        if 'current-password' in form and 'new-password' in form:
            res = requests.post(f'{API_URL}/user/{current_user.id}',
                                data=json.dumps({'current-password': form.get('current-password'),
                                                'new-password': form.get('new-password')
                                                 }), headers={
                                    "Content-Type": "application/json",
                                    'Authorization': f'Bearer {session.get("token")}'})
            g.res_status_code = res.status_code
            if res.status_code == 200:
                return render_template('profile-layout.html', user=g.user_info)
            else:
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


@app.route("/courses", methods=['GET', 'POST'])
@login_required
@is_token_valid
def course_page():
    '''Course(s) page'''
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
    '''Lessons under each course'''
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
    '''Delete lesson'''
    if current_user.role == 'user':
        return redirect(url_for('course_page'))
    res = requests.delete(
        f'{API_URL}//lesson/{course_name}/{lesson_id}',
        headers={"Authorization": f"Bearer {session.get('token')}"})
    if res.status_code != 410:
        g.res_error = res.json().get('msg')
    return redirect(url_for('lesson_page', course_name=course_name))


@app.route('/create-course', methods=['GET', 'POST'])
@login_required
@is_token_valid
def create_course():
    '''Create new course'''
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
                    data['course-image'] = save_image_to_db(image_file=image)[0]
                except Exception as e:
                    pass
        try:
            res = requests.post(f'{API_URL}/new-course',
                                data=json.dumps(data), headers={'Content-Type': 'application/json',
                                                                'Authorization': f'Bearer {session.get("token")}'})
            g.res_status_code = res.status_code
            if res.status_code != 201:
                g.res_error = res.json().get('msg')
        except Exception as e:
            pass
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
                data['image'] = save_image_to_db(image_file=image)[0]

            except Exception as e:
                pass
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
    res = requests.delete(f'{API_URL}/delete-course/{course_name}',
                          headers={'Authorization': f'Bearer {session.get("token")}'})
    g.res_status_code = res.status_code
    if res.status_code != 410:
        g.res_error = res.json().get('msg')
    return redirect(url_for('course_page'))


@app.route('/new-lesson', methods=['GET', 'POST'])
@login_required
@is_token_valid
def add_lesson():
    '''Create a new lesson under a course'''
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
    '''Edit a lesson'''
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


@app.route("/add-quiz", methods=['GET', 'POST'])
@login_required
@is_token_valid
def create_quiz():
    '''Add new quiz. Restricted to the admin'''
    if current_user.role != 'admin':
        return redirect(url_for('course_page'))
    if request.method == 'POST' and 'submit-new-quiz' in request.form:
        form = request.form
        data = {}
        data['quiz_name'] = form.get('quiz_name')
        data['description'] = form.get('description')
        if not db._DB__session.query(AvailableQuizes).filter(AvailableQuizes.quiz_name == form.get('quiz_name')).first():
            image = request.files.get('quiz_image')
            if image and image.filename:
                try:
                    data['quiz_image'] = save_image_to_db(image)[0]
                except Exception as e:
                    pass
        try:
            res = requests.post(f'{API_URL}/new-quiz', data=json.dumps(data), headers={'Content-Type': 'application/json',
                                                                                       'Authorization': f'Bearer {session.get("token")}'})
            g.res_status_code = res.status_code
            if res.status_code != 201:
                g.res_error = res.json().get('msg')
        except Exception as e:
            g.res_error = e.args[0]
    return render_template('create-quiz.html')


@app.route("/quizzes", methods=['GET', 'POST'])
@login_required
@is_token_valid
def quizzes_page():
    '''All quizzes page'''
    try:
        res = requests.get(f'{API_URL}/available-quizes')
        g.available_quizes = res.json()
    except Exception as e:
        pass
    return render_template('quizes-page.html')


@app.route('/edit-quiz/<quiz_name>/<quiz_id>', methods=['PUT', 'POST', 'GET'])
@login_required
@is_token_valid
def edit_quiz(quiz_name, quiz_id):
    '''Edit a course description and image if available'''
    form = request.form
    if request.method == 'POST' and 'edit-quiz-submit' in form:
        data = {'description': form.get('description')}
        image = request.files.get('quiz_image')
        if image and image.filename:
            try:
                data['quiz_image'] = save_image_to_db(image)
            except Exception as e:
                print(e)
        res = requests.put(f'{API_URL}/available-quiz/{quiz_id}',
                           data=json.dumps(data), headers={
                               'Content-Type': 'application/json',
                               'Authorization': f'Bearer {session.get("token")}'
                           })
        g.res_status = res.status_code
        if res.status_code != 200:
            g.res_error = res.json().get('msg')
    return redirect(url_for('quizzes_page'))


@app.route('/delete-quiz/<quiz_name>', methods=['GET', 'DELETE'])
@login_required
@is_token_valid
def delete_quiz(quiz_name):
    """Delete quiz. This drop the quiz table from the database"""
    res = requests.delete(f'{API_URL}/delete-quiz/{quiz_name}',
                          headers={'Authorization': f'Bearer {session.get("token")}'})
    g.res_status_code = res.status_code
    if res.status_code != 410:
        g.res_error = res.json().get('msg')
    return redirect(url_for('quizzes_page'))


@app.route('/new-quiz', methods=['GET', 'POST'])
@login_required
@is_token_valid
def add_quiz():
    '''Create a new quizs'''
    if current_user.role == 'user':
        return redirect(url_for('quizzes_page'))
    form = request.form
    if request.method == 'POST' and 'add-quiz-submit' in form:
        quiz_name = form.get('quiz_name')
        try:
            res = requests.post(f'{API_URL}/quiz/{quiz_name}',
                                data=json.dumps(form), headers={'Content-Type': 'application/json',
                                                                'Authorization': f'Bearer {session.get("token")}'})
            g.res_status_code = res.status_code
        except Exception as e:
            pass
    return render_template('quiz-content-creation.html')


@app.route("/quiz/<quiz_name>", methods=['GET', 'POST'])
@login_required
@is_token_valid
def quiz_page(quiz_name):
    '''Quiz question page for the quiz selected'''
    g.quiz_table = db._DB__session.query(AvailableQuizes).filter(
        AvailableQuizes.quiz_name == quiz_name).first()
    if not g.quiz_table:
        return redirect(url_for('quizzes_page'))
    try:
        res = requests.get(
            f'{API_URL}/quiz-table/{quiz_name}', headers={"Authorization": f"Bearer {session.get('token')}"})
        if res.status_code == 200:
            g.quizzes = res.json().get('quizzes')
            g.concepts = res.json().get('concepts')
            g.quiz_name = str(quiz_name).capitalize()
        else:
            g.res_error = res.json().get('msg')
    except Exception as e:
        pass

    return render_template('quiz-page.html')


@app.route('/request-password-reset', methods=['POST', 'GET'])
def reset_request():
    '''Request password reset'''
    if current_user.is_authenticated:
        return redirect(url_for('new_feed'))
    form = request.form
    if request.method == 'POST' and 'request-reset-btn' in form:
        user = db._DB__session.query(User).filter(
            User.email == form.get('email')).first()
        if user:
            g.msg = 'An email has been sent with the instructions to reset your password'
            send_reset_email(user)
            return redirect(url_for('sign_in'))
        else:
            g.msg = 'Email is invalid!'
    return render_template('reset_request.html')


@app.route('/reset-password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    '''Request password reset'''
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = request.form
    user = User.verify_reset_token(db, User, app, token)
    if user is None:
        g.msg = 'That is an invalid or expired token'
        return redirect(url_for('request_reset'))
    if request.method == 'POST' and 'reset-password-tk-btn' in form:
        user.password = form.get('password')
        g.msg = 'Password has been changed successfully!'
        db.save()
        return redirect(url_for('sign_in'))
    return render_template('reset_password.html', token=token)


@app.get('/')
@app.get('/landing-page')
def landing_page():
    '''Welcome page'''
    if current_user.is_authenticated:
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('landing_page.html')


@app.errorhandler(404)
def page_not_found(error):
    '''404 page'''
    return render_template('404.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    '''log out'''
    session.clear()
    logout_user()
    return redirect(url_for('landing_page'))


@login_manager.unauthorized_handler
def unauthorized_user():
    '''On unauthorized user'''
    return redirect(url_for('sign_in'))


if __name__ == '__main__':
    '''Main'''
    app.run()
