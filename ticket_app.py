### Ticket App ###

from flask import Flask, render_template, session, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
SECRET_KEY = "SECRET"
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "sqlite:///db.db")
db = SQLAlchemy(app)
@app.route("/")
def index():
    from models import User
    if "user" in session:
        return User.query.get(session['user']).email
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    from models import User
    if 'email' in request.form and 'password' in request.form:
        user = User.query.filter_by(email=request.form['email']).first()
        if user.validate_password(request.form['password']):
            session['user'] = str(user.id)
            return "You are Logged in!"
    return "Login Failed!"



if __name__=="__main__":
    app.run(debug=True)
    


