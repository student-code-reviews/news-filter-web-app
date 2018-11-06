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


@app.route('/news-options')
def news_options():
    """ This displays a page with following news options- world, technology, politics, entertainment"""

    return render_template('news_options.html')


@app.route('/headlines', methods=['POST'])
def headlines():
    top_headlines = newsapi.get_top_headlines(q='',
                                              sources='bbc-news,the-verge',
                                              language='en')
    headlines = top_headlines['articles']
    if not headlines:
        # This is when an empty list of news is returned after API request
        result = 'No headlines found.'
    else:
        result = 'Found following news:'
    return render_template('headlines.html', result=result, articles=headlines)


@app.route('/filterednews', methods=['POST'])
def filterednews():
    """Returns triggering news based on the keyword passed"""
    news_type = request.form.get("option")
    app.logger.info(news_type)
    if news_type == 'world':
        news = 'world'
        trigger_word = 'trump'
    else:
        trigger_word = 'trump'
    all_articles = newsapi.get_everything(q='+{}'.format(trigger_word),
                                          sources='the-wall-street-journal',
                                          from_param='2018-10-05',
                                          to='2018-11-05',
                                          language='en',
                                          sort_by='relevancy',
                                          page=2)
    articles = all_articles['articles']
    if not articles:
        # This is when an empty list of news is returned after API request
        result = 'No triggering news found.'
    else:
        result = 'Found following news'

    return render_template('filtered_news.html', result=result, articles=articles)


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
