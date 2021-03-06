### Ticket App ###

from flask import Flask, render_template, session, request, redirect, flash
from flask.ext.sqlalchemy import SQLAlchemy
# import all of models to get around circular import error
import models
import os
from datetime import datetime


SECRET_KEY = "SECRET"
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///db.db')
db = SQLAlchemy(app)


def get_model(user_models, user_string):
    if (user_string in session):
        return user_models.query.get(session[user_string])
    else:
        return None


def index(user_models, user_string, template, events=None):
    user = get_model(user_models, user_string)
    return render_template(template, user=user, events=events)


def login(user_models, user_string, next_url='/'):
    if request.form.get('email') and request.form.get('password'):
        user = user_models.get_by_email(request.form['email'])
        if user.validate_password(request.form['password']):
            if 'group' in session:
                del session['group']
            if 'student' in session:
                del session['student']
            session[user_string] = str(user.id)
        else:
            flash("Email or Password Invalid")
    else:
        flash("Email and Password are Required")
    return redirect(next_url)


def signup(user_models, user_string, next_url='/'):
    try:
        user = user_models(request.form.get('name'),
                           request.form.get('email'),
                           request.form.get('password'),
                           request.form.get('confirm_password'))
        db.session.add(user)
        db.session.commit()
        db.session.flush()
        session[user_string] = str(user.id)
    except models.UserError as e:
        flash(str(e))
    return redirect(next_url)


def logout(user_string, next_url='/'):
    del session[user_string]
    return redirect(next_url)


@app.route("/")
def student_index():
    #Groups do not need to be on the Student Listings page
    if 'group' in session:
        del session['group']
    return index(models.Student, 'student', 'index.html',
                 models.Event.query.all())


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


@app.route('/create_event', methods=['POST'])
def create_event():
    group = get_model(models.Group, 'group')
    frmt = "%m/%d/%y %I:%M %p"
    if group:
        try:
            date_time = (request.form.get('date') + " " +
                         request.form.get('time'))
            event = models.Event(request.form.get('name'),
                                 request.form.get('description'),
                                 datetime.strptime(date_time, frmt), group,
                                 request.form.get('max_attendees'),
                                 request.form.get('ticket_price'))
            group.query.session.add(event)
            group.query.session.commit()
            group.query.session.flush()
        except models.EventError as e:
            flash(str(e))
    else:
        flash("Must Be Logged In to Create an Event")
    return redirect('/group')


@app.route("/event/<event_id>", methods=['GET'])
def view_event(event_id):
    event = models.Event.query.get(event_id)
    attendees = len(event.attendees.all())
    user = get_model(models.Student, 'student')
    group = get_model(models.Group, 'group')
    if group is not None:
        return render_template('group_view_event.html', event=event,
                               user=group, attendees=attendees)
    else:
        return render_template('view_event.html', event=event, user=user)


@app.route('/event_delete/<event_id>', methods=['POST'])
def delete_event(event_id):
    event_del = models.Event.query.get(event_id)
    if event_del:
        group = get_model(models.Group, 'group')
        if group:
            if event_del.group == group:
                models.Event.query.session.delete(event_del)
                models.Event.query.session.commit()
                models.Event.query.session.flush()
                return redirect('/group')
        flash("You do not have permission to delete this event")
        return redirect('/event/' + event_id)
    else:
        flash("Sorry you cannot delete the event at this time")
        return redirect('/event/' + event_id)


@app.route("/group_event/<event_id>", methods=['GET'])
def group_view_event(event_id):
    event = models.Event.query.get(event_id)
    return render_template('group_view_event.html', event=event)


@app.route("/event/<event_id>/purchase", methods=['POST'])
def attending_event(event_id):
    student = get_model(models.Student, 'student')
    if student:
        event = models.Event.query.get(event_id)
        event.attendees.append(student)
        event.query.session.commit()
        flash("Enjoy the Event!")
    else:
        flash("You must be logged in to purchase a ticket")
    return redirect("/event/" + event_id)


@app.route("/group/<event_id>/printable_attendee_list")
def get_attendee_list(event_id):
    event = models.Event.query.get(event_id)
    return render_template('print_attendees.html', event=event)


@app.route('/leaderboard')
def leader_board():
    current_date = datetime.now()
    this_week = models.Event.all()
    happening = list()
    for event in this_week:
        diff = (event.date - current_date).total_seconds()
        if diff <= 604800 and diff >= 0:
            happening.append(event)
    return render_template('leaderboard.html', leaders=this_week)


def datetime_to_str(date):
    frmt = "%I:%M %p, %m/%d/%y"
    return date.strftime(frmt)


def sort_events(events):
    return sorted(events, key=lambda e: e.date)

app.jinja_env.globals.update(datetime_to_str=datetime_to_str,
                             sort_events=sort_events)

if __name__ == "__main__":
    app.run(debug=True)
