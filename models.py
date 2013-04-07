# Models for Ticket App #
from flask import session, request, g
import bcrypt
from ticket_app import db
class UserException(Exception):

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
            raise UserException("No Username given")
        if password:
            if password == confirm_password:
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                self.email = email
                self.hash = hashed_password
            else:
                raise UserException("Passwords do not match")
        else:
            raise UserException("Enter Password")

    def validate_password(self, password):
        return bcrypt.hashpw(password, self.hash) == self.hash
