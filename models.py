# Models for Ticket App #
from flask import session, request, g
import bcrypt
from ticket_app import db

class UserError(Exception):

    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True) 
    hash = db.Column(db.String())

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


#TODO: Make mixin
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    _user = db.relationship("User", backref=db.backref("student", uselist=False))

    def __init__(self, email, password, confirm_password):
        self._user = User(email, password, confirm_password)

    @property
    def email(self):
        return self._user.email

    def validate_password(self, password):
        return self._user.validate_password(password)

    @staticmethod
    def student_with_email(email):
        user = User.query.filter_by(email=email).first()
        return user.student


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    _user = db.relationship("User", backref=db.backref("group", uselist=False))

    def __init__(self, email, password, confirm_password):
        self._user = User(email, password, confirm_password)

    @property
    def email(self):
        return self._user.email

    def validate_password(self, password):
        return self._user.validate_password(password)

    @staticmethod
    def group_with_email(email):
        user = User.query.filter_by(email=email).first()
        return user.group
