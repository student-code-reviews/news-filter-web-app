"""Filtered News"""
# Please note that the word trigger itself can elicit negative feelings. To address this,
# I have used only letter t
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
        user = User.query.filter(User.email == session['user']).one()
        user_id = int(user.user_id)
        return render_template("log_in_homepage.html", user_id=user_id)
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
        # tr_words is a string. For now, it is only one word.
        trig_word = request.form.get("trig_word")

        user_list = db.session.query(User.email).all()

        if user_email not in user_list:
            new_user = User(email=user_email, password=user_password, trig=trig_word)
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

    # If the check works for the email and matching password, news options page is rendered.
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


@app.route('/filtered-news/<user_id>', methods=['POST'])
def filterednews(user_id):
    """Returns triggering news based on the user's preferences """

    news_type = request.form.get("option")

    # Making a user object to access trigger word for that user.
    user = User.query.get('{}'.format(user_id))
    trig_word = user.trig
    topic = ''
    # Based on user's preference of news section, providing section news.
    if news_type == 'world':
        domains = 'thehindu.com, bbc.co.uk, nytimes.com'
    elif news_type == 'technology':
        domains = 'techcrunch.com, theverge.com, hackernews.com'
    elif news_type == 'politics':
        domains = 'politico.com'
    elif news_type == 'entertainment':
        domains = 'ew.com'
    else:
        sources = 'espn'
        domains = 'espn.com'

    all_articles = newsapi.get_everything(q=f'-{trig_word}',
                                          domains=domains,
                                          from_param=f'{date.today()}',
                                          to=f'{date.today()}',
                                          language='en')

    articles = all_articles['articles']
    if not articles:
        # This is when an empty list of news is returned after API request
        result = 'No news found.'
    else:
        result = "Today's news"

    return render_template('filtered_news.html', user=user, result=result, articles=articles, news=news_type, user_id=user_id)


@app.route('/trig-tagged-news/<user_id>', methods=['POST'])
def trig_tagging_news(user_id):
    """Gets the title of triggering article and returns a page with a list of
    triggering words that the user can choose from. """

    trig_article = request.form.get("trig_article")
    app.logger.info(trig_article)
    return render_template('triggered.html', trig_article=trig_article)


@app.route('/trig-submitted/<trig_article>', methods=['POST'])
def trig_tagging(trig_article):
    """Adds the triggering article and trigger word associated with it to the db"""

    # Getting a list of news objects:
    trig_news = db.session.query(News.trig_article).all()

    # Checking if triggering article is already in the database. If it isn't,
    # adding the article to the news table.
    if trig_article not in trig_news:
        trig_words = request.form.get("trig_words")
        new_trig_article = News(trig_article=trig_article, trig_words=trig_words)
        db.session.add(new_trig_article)
        db.session.commit()

    return render_template('trigger_submitted.html')


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
