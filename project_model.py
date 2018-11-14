""" Models and database functions for project db """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import date

db = SQLAlchemy()


class User(db.Model):
    """ User's details like username, password and triggering workds"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.Binary, nullable=True)
    trig = db.Column(ARRAY(db.String(100)), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<User {} user_id={} triggers={}>".format(username=self.email, user_id=self.user_id, trigger=self.trig)


class BannedNews(db.Model):
    """ News with news id. """

    __tablename__ = 'bannednews'

    news_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trig_article = db.Column(db.String(200), nullable=False)
    trig_words = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return f"<News_id={self.news_id} triggers={self.trig_words} date_added={self.trig_words}>"


# -------------------------------------------------------------------
# Helper functions


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///filterednews'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.app = app
    # db.init_app(app)


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    BannedNews.query.delete()

    # Add sample employees and departments
    news1 = BannedNews(news_id=1,
                       trig_article='This is an examle',
                       trig_words='rape, war',
                       date_added=date.today())
    news2 = BannedNews(news_id=1,
                       trig_article='This is an examle',
                       trig_words='assault',
                       date_added=date.today())
    news3 = BannedNews(news_id=1,
                       trig_article='This is an examle',
                       trig_words='rape, trump',
                       date_added=date.today())

    user1 = User(name='Leonard', dept=dl)
    user2 = User(name='Liz', dept=dl)
    user3 = User(name='Maggie', dept=dm)

    db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()
