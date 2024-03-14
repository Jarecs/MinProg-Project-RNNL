from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from . import newrnnl
from ..models import User, Event
from .forms import ProfileForm, EventForm


@newrnnl.route('/')
def index():
    return render_template('newrnnl/index.html')


@newrnnl.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        db.create_all()
        event = Event(
            name=form.event_name.data,
            description=form.event_description.data,
            location=form.event_location.data,
            date=form.event_date.data,
            time=form.event_time.data,
            is_private=form.event_is_private.data,
            password=form.event_password.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('.index'))
    return render_template('newrnnl/create.html', form=form)


@newrnnl.route('/find')
@login_required
def find():
    return render_template('newrnnl/find.html')


@newrnnl.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('newrnnl.index'))
    form.name.data = current_user.name
    form.location.data = current_user.location
    return render_template("newrnnl/profile.html", form=form)

# @newrnnl.route('/', methods=['GET', 'POST'])
# def login_form():
#     # Forget any user_id
#     session.clear()
#
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = Users.query.filter_by(username=username).first()
#         logging.info(user)
#         if user.username == username and check_password_hash(user.hash, password):
#             session['username'] = username
#             return flask.redirect("home")
#         else:
#             return flask.render_template("login.html", error="Invalid username or password")
#
#     return flask.render_template("login.html")
#
#
# @newrnnl.route('/register', methods=['GET', 'POST'])
# def register_form():
#     if request.method == "GET":
#         return render_template("register.html")
#     else:
#         username = request.form.get("username")
#         password = request.form.get("password")
#         confirmation = request.form.get("confirmation")
#         if not username:
#             return flask.render_template("register.html", error="Fill in a Username")
#         if not password or not confirmation:
#             return flask.render_template("register.html", error="Fill in a Password and Confirmation")
#         if password != confirmation:
#             return flask.render_template("register.html", error="Passwords do not match")
#         hash = generate_password_hash(password)
#
#         user = Users(username=username, hash=hash)
#         try:
#             db.session.add(user)
#             db.session.commit()
#         except:
#             return flask.render_template("register.html", error="Username already exists")
#         session["username"] = username
#         return flask.redirect("home")
#
#
# @newrnnl.route("/home", methods=['GET', 'POST'])
# @login_required
# def home():
#     return flask.render_template("home.html", username=session['username'])
#
#
# @newrnnl.route("/create", methods=['GET', 'POST'])
# def create_game():
#     form = EventForm()
#     if form.validate_on_submit():
#         event = Events(
#             date=form.date.data,
#             location=form.location.data,
#             player_limit=form.player_limit.data,
#             private=form.private.data,
#             password=form.password.data
#         )
#         db.session.add(event)
#         db.session.commit()
#         return flask.redirect("home")  # Redirect to the home page or any other page
#     return render_template('create.html', form=form)
#
#
# @newrnnl.route("/find", methods=['GET', 'POST'])
# @login_required
# def find_game():
#     all_events = Events.query.all()
#
#     # Render the template with the events data
#     return render_template('find.html', events=all_events)
#
#
# @newrnnl.route("/profile", methods=['GET', 'POST'])
# @login_required
# def profile():
#     return flask.render_template("profile.html")
#
#
# @newrnnl.route("/test_function_1", methods=["GET"])
# @login_required
# def test_function_1():
#     return flask.render_template("profile.html", firstValue="test_function_1 called")
#
#
# @newrnnl.route("/test_function_2", methods=["GET"])
# @login_required
# def test_function_2():
#     return flask.render_template("profile.html", secondValue="hey")
