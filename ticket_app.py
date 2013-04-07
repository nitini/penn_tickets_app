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
    from models import User
    user = None
    if "user" in session:
        user = User.query.get(session['user'])
    return render_template('index.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    from models import User
    if request.form.get('email') and request.form.get('password'):
        user = User.query.filter_by(email=request.form['email']).first()
        if user.validate_password(request.form['password']):
            session['user'] = str(user.id)
            flash("You are Logged in!")
        else:
            flash("Email or Password Invalid")
    else:
        flash("Email and Password are Required")
    return redirect("/")


@app.route('/signup', methods=['POST'])
def signup():
    from models import User, UserError
    try:
        user = User(request.form.get('email'), request.form.get('password'), request.form.get('confirm_password'))
        db.session.add(user)
        db.session.commit()
    except UserError as e:
        flash(str(e))
    return redirect("/")

@app.route('/logout')
def logout():
    del session['user']
    flash("You are Logged Out!")
    return redirect("/")




if __name__=="__main__":
    app.run(debug=True)
    


