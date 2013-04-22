# Models for Ticket App #
import bcrypt
import datetime
import ticket_app as app


class UserError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class User(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    name = app.db.Column(app.db.String(80))
    email = app.db.Column(app.db.String(120), unique=True)
    hash = app.db.Column(app.db.String())

    def __init__(self, email, password, confirm_password):
        if not email:
            raise UserError("No Username given")
        if password:
            if password == confirm_password:
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                self.email = email
                self.hash = hashed_password
            else:
                raise UserError("Passwords do not match")
        else:
            raise UserError("Enter Password")

    def validate_password(self, password):
        return bcrypt.hashpw(password, self.hash) == self.hash


class TicketUser():
    def __init__(self, email, password, confirm_password):
        self._user = User(email, password, confirm_password)

    @property
    def email(self):
        return self._user.email

    def validate_password(self, password):
        return self._user.validate_password(password)


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


class Event(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    name = app.db.Column(app.db.String(80))
    date = app.db.DateTime()
    group_id = app.db.Column(app.db.Integer, app.db.ForeignKey('group.id'))
    description = app.db.Column(app.db.String(500))

    def __init__(self, name, description, group):
        self.name = name
        self.group = group
        self.date = datetime.datetime.now()
        self.description = description
