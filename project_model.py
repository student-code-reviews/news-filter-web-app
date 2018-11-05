""" Models and database functions for project db """


from flask_sqlalchemy import SQLalchemy
# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)
db = SQLalchemy


class User:
    """ User's details like username, password and triggering workds"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    triggers = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<User {username} user_id={user_id} triggers={}>".format(username=self.username, user_id=self.user_id, tirggers=self.triggers)


class News:
    """ News with news id. """

    __tablename__ = 'news'

    news_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trigger_words = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<News_id={} triggers={}>".format(news_id=self.news_id, self.trigger_words)


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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///news'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()
