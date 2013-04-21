### Ticket App ###

from flask import Flask, render_template, session, request, redirect, flash
from flask.ext.sqlalchemy import SQLAlchemy
import os
SECRET_KEY = "SECRET"
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "sqlite:///db.db")
db = SQLAlchemy(app)

@app.route("/")
def index():
    from models import Student
    student = None
    if 'student' in session:
        student = Student.query.get(session['student'])
    return render_template('index.html', student=student)

@app.route('/login', methods=['POST'])
def login():
    from models import Student
    if request.form.get('email') and request.form.get('password'):
        student = Student.student_with_email(request.form['email'])
        if student.validate_password(request.form['password']):
            if 'group' in session:
                del session['group']
            session['student'] = str(student.id)
            flash("You are Logged in!")
        else:
            flash("Email or Password Invalid")
    else:
        flash("Email and Password are Required")
    return redirect("/")


@app.route('/signup', methods=['POST'])
def signup():
    from models import Student, UserError
    try:
        student = Student(request.form.get('email'), request.form.get('password'), request.form.get('confirm_password'))
        db.session.add(student)
        db.session.commit()
    except UserError as e:
        flash(str(e))
    return redirect("/")

@app.route('/logout')
def logout():
    del session['student']
    flash("You are Logged Out!")
    return redirect("/")

@app.route('/group')
def group():
    from models import Group
    group = None
    if 'group' in session:
        group = Group.query.get(session['group'])
    return render_template('group.html', group=group)

@app.route('/group_login', methods=['POST'])
def group_login():
    from models import Group
    if request.form.get('email') and request.form.get('password'):
        group = Group.group_with_email(request.form['email'])
        if group.validate_password(request.form['password']):
            if 'student' in session:
                del session['student']
            session['group'] = str(group.id)
            flash("You are Logged in!")
        else:
            flash("Email or Password Invalid")
    else:
        flash("Email and Password are Required")
    return redirect("/group")


@app.route('/group_signup', methods=['POST'])
def group_signup():
    from models import Group, UserError
    try:
        group = Group(request.form.get('email'), request.form.get('password'), request.form.get('confirm_password'))
        db.session.add(group)
        db.session.commit()
    except UserError as e:
        flash(str(e))
    return redirect("/group")

@app.route('/group_logout')
def group_logout():
    del session['group']
    flash("You are Logged Out!")
    return redirect("/group")

if __name__=="__main__":
    app.run(debug=True)
