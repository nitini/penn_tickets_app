### Ticket App ###

from flask import Flask, render_template, session, request, redirect, flash
from flask.ext.sqlalchemy import SQLAlchemy
import models
import os
SECRET_KEY = "SECRET"
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///db.db')
db = SQLAlchemy(app)


def index(user_models, user_string, template):
    user = None
    if user_string in session:
        user = user_models.query.get(session[user_string])
    return render_template(template, user=user)


def login(user_models, user_string, next_url='/'):
    if request.form.get('email') and request.form.get('password'):
        user = user_models.get_by_email(request.form['email'])
        if user.validate_password(request.form['password']):
            if 'group' in session:
                del session['group']
            if 'student' in session:
                del session['student']
            session[user_string] = str(user.id)
            flash("You are Logged in!")
        else:
            flash("Email or Password Invalid")
    else:
        flash("Email and Password are Required")
    return redirect(next_url)


def signup(user_models, user_string, next_url='/'):
    try:
        user = user_models(request.form.get('email'),
                           request.form.get('password'),
                           request.form.get('confirm_password'))
        db.session.add(user)
        db.session.commit()
    except models.UserError as e:
        flash(str(e))
    return redirect(next_url)


def logout(user_string, next_url='/'):
    del session[user_string]
    flash("You are Logged Out!")
    return redirect(next_url)


@app.route("/")
def student_index():
    return index(models.Student, 'student', 'index.html')


@app.route('/login', methods=['POST'])
def student_login():
    return login(models.Student, 'student')


@app.route('/signup', methods=['POST'])
def student_signup():
    return signup(models.Student, 'student')


@app.route('/logout')
def student_logout():
    return logout('student')


@app.route('/group')
def group():
    return index(models.Group, 'group', 'group.html')


@app.route('/group_login', methods=['POST'])
def group_login():
    return login(models.Group, 'group', '/group')


@app.route('/group_signup', methods=['POST'])
def group_signup():
    return signup(models.Group, 'group', '/group')


@app.route('/group_logout')
def group_logout():
    return logout('group', '/group')


@app.route('/events')
def events():
    return str(models.Event.query.all()[0])


if __name__ == "__main__":
    app.run(debug=True)
