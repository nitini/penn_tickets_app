# Models for Ticket App #
import bcrypt
from datetime import *
import ticket_app as app


class UserError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class EventError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class User(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    name = app.db.Column(app.db.String(80))
    email = app.db.Column(app.db.String(120), unique=True)
    hash = app.db.Column(app.db.String())

    def __init__(self, name, email, password, confirm_password):
        if not email or not name:
            raise UserError("No Name or Email given")
        if password:
            if password == confirm_password:
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                self.name = name
                self.email = email
                self.hash = hashed_password
            else:
                raise UserError("Passwords do not match")
        else:
            raise UserError("Enter Password")

    def validate_password(self, password):
        return bcrypt.hashpw(password, self.hash) == self.hash


class TicketUser():
    def __init__(self, name, email, password, confirm_password):
        self._user = User(name, email, password, confirm_password)

    @property
    def email(self):
        return self._user.email

    @property
    def name(self):
        return self._user.name

    def validate_password(self, password):
        return self._user.validate_password(password)

    def __repr__(self):
        return self.email


class Student(TicketUser, app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    _user_id = app.db.Column(app.db.Integer, app.db.ForeignKey('user.id'))
    _user = app.db.relationship("User", backref=app.db.backref("student",
                                                               uselist=False))
    @staticmethod
    def get_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user.student

class Group(TicketUser, app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    _user_id = app.db.Column(app.db.Integer, app.db.ForeignKey('user.id'))
    _user = app.db.relationship('User', backref=app.db.backref("group",
                                                               uselist=False))
    events = app.db.relationship('Event', backref='group', lazy='dynamic')

    @staticmethod
    def get_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user.group
    
attendances = app.db.Table('attendances',
                           app.db.Column('event_id', app.db.Integer,
                                         app.db.ForeignKey('event.id')),
                           app.db.Column('student_id', app.db.Integer,
                                         app.db.ForeignKey('student.id')))


class Event(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    name = app.db.Column(app.db.String(80))
    date = app.db.Column(app.db.DateTime(timezone=False))
    group_id = app.db.Column(app.db.Integer, app.db.ForeignKey('group.id'))
    description = app.db.Column(app.db.String(500))
    max_attendees = app.db.Column(app.db.Integer())
    ticket_price = app.db.Column(app.db.String(80))

    attendees = app.db.relationship('Student', secondary=attendances,
                                    lazy='dynamic',
                                    backref=app.db.backref('events',
                                                           lazy='dynamic'))

    def __init__(self, name, description, date,  group, max_attendees,
                 ticket_price):
        self.name = name
        self.group = group
        self.date = date
        self.description = description
        self.max_attendees = max_attendees
        self.ticket_price = ticket_price
        self.count = 0

    def __repr__(self):
        return self.name + " - " + self.description
