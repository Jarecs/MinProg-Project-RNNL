import logging

import flask
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from flask_wtf import FlaskForm
from wtforms import DateField, StringField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email

from functools import wraps


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rnnl_test.db'
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your_secret_key_here'
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return flask.redirect("/")
        return f(*args, **kwargs)
    return decorated_function

class EventForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    player_limit = IntegerField('Amount of Players', validators=[DataRequired()])
    private = BooleanField('Private Event')
    password = PasswordField('Event Password')

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    hash = db.Column(db.String(256))

    def __repr__(self):
        return f'<User {self.username}>'

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    location = db.Column(db.String(80))
    player_limit = db.Column(db.Integer, default=4)
    private = db.Column(db.Boolean, default=True)
    password = db.Column(db.String(256))



EventPlayer = db.Table('event_player',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

db.create_all()


@app.route('/', methods=['GET', 'POST'])
def login_form():
    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        logging.info(user)
        if user.username == username and check_password_hash(user.hash, password):
            session['username'] = username
            return flask.redirect("home")
        else:
            return flask.render_template("login.html", error="Invalid username or password")

    return flask.render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register_form():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return flask.render_template("register.html", error="Fill in a Username")
        if not password or not confirmation:
            return flask.render_template("register.html", error="Fill in a Password and Confirmation")
        if password != confirmation:
            return flask.render_template("register.html", error="Passwords do not match")
        hash = generate_password_hash(password)

        user = Users(username=username, hash=hash)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return flask.render_template("register.html", error="Username already exists")
        session["username"] = username
        return flask.redirect("home")


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return flask.render_template("home.html", username=session['username'])


@app.route("/create", methods=['GET', 'POST'])
def create_game():
    form = EventForm()
    if form.validate_on_submit():
        event = Events(
            date=form.date.data,
            location=form.location.data,
            player_limit=form.player_limit.data,
            private=form.private.data,
            password=form.password.data
        )
        db.session.add(event)
        db.session.commit()
        return flask.redirect("home")  # Redirect to the home page or any other page
    return render_template('create.html', form=form)


@app.route("/find", methods=['GET', 'POST'])
@login_required
def find_game():
    all_events = Events.query.all()

    # Render the template with the events data
    return render_template('find.html', events=all_events)


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    return flask.render_template("profile.html")


@app.route("/test_function_1", methods=["GET"])
@login_required
def test_function_1():
    return flask.render_template("profile.html", firstValue="test_function_1 called")

@app.route("/test_function_2", methods=["GET"])
@login_required
def test_function_2():
    return flask.render_template("profile.html", secondValue="hey")


if __name__ == "__main__":
    app.run(debug=True)
