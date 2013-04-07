### Ticket App ###

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "sqlite:///db.db")
db = SQLAlchemy(app)
@app.route("/")
def index():
    return "Hellooo"

if __name__=="__main__":
    app.run(debug=True)
    


