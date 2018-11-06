""" Models and database functions for project db """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ User's details like username, password and triggering workds"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    trigger = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<User {} user_id={} triggers={}>".format(username=self.email, user_id=self.user_id, trigger=self.trigger)


class News(db.Model):
    """ News with news id. """

    __tablename__ = 'news'

    news_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trigger_words = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<News_id={} triggers={}>".format(news_id=self.news_id, triggers=self.trigger_words)


# -------------------------------------------------------------------
# Helper functions


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///filterednews'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()
