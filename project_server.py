"""Filtered News"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from project_model import User, News, connect_to_db, db

from newsapi import NewsApiClient

import requests

newsapi = NewsApiClient(api_key='f137fa32c38e47849487b4231fee31b0')

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

# Here, we are checking if the user is logged in (session has 'user' key)
    if 'user' in session:
        return render_template("log_in_homepage.html")
    else:
        return render_template("homepage.html")


@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """Registration form that takes email address, password and trigger words."""

    # Reg form is rendered when you go to page. When it is submitted, a post request is made and if user's email is not in database then it gets added and redirected to the
    # homepage.
    if request.method == 'GET':
        return render_template("registration_form.html")

    else:
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        # Trigger_words is a string.
        trigger_words = reqest.form.get("trigger_words")

        user_list = db.session.query(User.email).all()

        if user_email not in user_list:
            new_user = User(email=user_email, password=user_password, triggers=trigger_words)
            db.session.add(new_user)
            db.session.commit()

        return redirect("/")


@app.route('/login')
def login():
    """Login Page."""

    return render_template("login.html")


@app.route('/logged-in', methods=['POST'])
def logged_in():
    """Logged in or not"""

    email = request.form.get("email")
    password = request.form.get("password")

    # Checking to see if this email exists in the database. Making a user object.
    user = User.query.filter(User.email == email).one()

    # Checking to see if the password matches for the email provided by the user.
    user_check = User.query.filter(User.email == email, User.password == password).all()

    # If the check works for the email and matching password, user details page is rendered.
    # Otherwise, the login page is rendered again.
    if user_check:
        session['user'] = email
        # User id is saved in this varianble.
        user_id = int(user.user_id)
        flash("You have successfully logged in!")
        return redirect(f"filtered-news/{user_id}")
    else:
        return redirect("/login")


@app.route('/logout')
def logout():
    """Logged out and session cleared."""

# This is how you clear a session. Very important when logging out.
    session.clear()
    flash("Logged out!")
    return redirect("/")


@app.route('/filtered-news/<user_id>')
def filtered_news(user_id):
    """Get filtered news based on the user's preferences"""
    pass


if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000)
