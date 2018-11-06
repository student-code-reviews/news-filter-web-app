"""Filtered News"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from project_model import User, News, connect_to_db, db

from newsapi import NewsApiClient

import requests

from datetime import date

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
        # Trigger_words is a string. For now, it is only one word.
        trigger_word = request.form.get("trigger_word")

        user_list = db.session.query(User.email).all()

        if user_email not in user_list:
            new_user = User(email=user_email, password=user_password, trigger=trigger_word)
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
        # User id is saved in this variable.
        user_id = int(user.user_id)
        flash("You have successfully logged in!")
        return redirect(f"news-options/{user_id}")
    else:
        return redirect("/login")


@app.route('/logout')
def logout():
    """Logged out and session cleared."""

# This is how you clear a session. Very important when logging out.
    session.clear()
    flash("Logged out!")
    return redirect("/")


@app.route('/news-options/<user_id>')
def news_options(user_id):
    """ This displays a page with following news options- world, technology, politics, entertainment"""
    app.logger.info(type(user_id))
    return render_template('news_options.html', user_id=user_id)


# @app.route('/headlines', methods=['POST'])
# def headlines():
#     top_headlines = newsapi.get_top_headlines(q='',
#                                               sources='bbc-news,the-verge',
#                                               language='en')
#     headlines = top_headlines['articles']
#     if not headlines:
#         # This is when an empty list of news is returned after API request
#         result = 'No headlines found.'
#     else:
#         result = 'Found following news:'
#     return render_template('headlines.html', result=result, articles=headlines)


@app.route('/filtered-news/<user_id>', methods=['POST'])
def filterednews(user_id):
    """Returns triggering news based on the keyword passed"""

    news_type = request.form.get("option")

    # Making a user object to access trigger word for that user.
    user = User.query.get('{}'.format(user_id))
    trigger_word = user.trigger

    # Based on user's preference of news section, providing section news.
    if news_type == 'world':
        news = 'world'
        sources = 'the-hindu, bbc-news, the-new-york'
    elif news_type == 'technology':
        news = 'technology'
        sources = 'techcrunch, techradar, the-verge, hacker-news'
    elif news_type == 'politics':
        news = 'politics'
        sources = 'politico'
    elif news_type == 'entertainment':
        news = 'entertainment'
        sources = 'entertainment-weekly'
    elif news_type == 'sports':
        news = 'sports'
        sources = 'espn, fox-sports'
    else:
        # For headlines
        top_headlines = newsapi.get_top_headlines(q='',
                                                  sources='the-wall-street-journal',
                                                  language='en')
        headlines = top_headlines['articles']
        if not headlines:
            # This is when an empty list of news is returned after API request
            result = 'No headlines found.'
        else:
            result = 'Found following news:'
        return render_template('headlines.html', result=result, articles=headlines)

    # This is for all articles in a perticular section without news with user's trigger word

    all_articles = newsapi.get_everything(q=f'-{trigger_word}',
                                          sources=sources,
                                          from_param=f'{date.today()}',
                                          to=f'{date.today()}',
                                          language='en',
                                          sort_by='relevancy',
                                          page=2)
    articles = all_articles['articles']
    if not articles:
        # This is when an empty list of news is returned after API request
        result = 'No triggering news found.'
    else:
        result = 'Found following news'

    return render_template('filtered_news.html', result=result, articles=articles, news=news, user_id=user_id)


@app.route('/trigger-tagged-news/<user_id>', methods=['POST'])
def trigger_tagging_news(user_id):
    """Returns triggering news based on the keyword passed"""

    triggering_article = request.form.get("trigger_article")
    app.logger.info(triggering_article)
    return render_template('triggered.html')


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
