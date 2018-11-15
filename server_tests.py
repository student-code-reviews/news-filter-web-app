from project_server import app, hash_password
import unittest
from project_server import app
from six import b, u
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project_model import User, BannedNews, db, connect_to_db
from datetime import date

######################################################################
# Tests that don't require the database nor an active session.
# Summary of tests in this section: homepage, log in page,
# register page.
######################################################################


class FlaskTests(unittest.TestCase):

    def setUp(self):
        """ Stuff to do before every test. """

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """ Test homepage when user is not logged in."""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Filtered News', result.data)

    def test_login_page(self):
        """ Test whether login page is displayed. """
        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Login here:', result.data)

    def test_register_page(self):
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"To register, please provide", result.data)


######################################################################
# Tests that require an active session, but no database access
######################################################################

class FlaskTestsSessionOn(unittest.TestCase):
    """ Flasks tests when session is on without
    database connection"""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'k@gmail.com'

    def test_logout(self):
        """ Test logout when user in session."""
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"Logged out!", result.data)


######################################################################
# Tests that require database access and an active session, but don't
# alter the state of the database.
######################################################################

class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Necessary before every test. Configures the app,
        creates client, connects to test database, creates
        the tables, and seeds the test database."""

        # Get the Flask test client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, uri='postgres:///testdb')

        # Create tables and add sample data
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'k@gmail.com'

    def tearDown(self):
        """Do at the end of every test"""

        db.session.close()
        db.drop_all()

    def test_logging_in(self):
        """ Tests if login function works and
        is able to access database."""

        result = self.client.post("/logged-in",
                                  data={"email": 'hello@gmail.com',
                                        "password": "hello"},
                                  follow_redirects=True)

        self.assertIn(b"You have successfully logged in!", result.data)

######################################################################
# Tests that require database access, need an active session, and
# can actually change the database.
######################################################################


class FlaskTestsChangeDB(unittest.TestCase):
    """Flask tests for changing database."""

    def setUp(self):
        """Necessary before every test. Configures the app,
        creates client, connects to test database, creates
        the tables, and seeds the test database."""

        # Get the Flask test client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, uri='postgres:///testdb')

        # Create tables and add sample data
        example_data()

    def tearDown(self):
        """Do at the end of every test"""

        db.session.close()
        # db.drop_all()

    def test_registration_form(self):
        """ Tests if user can register and save data
        into database."""

        result = self.client.post("/register",
                                  data={"email": "test@email.com",
                                        "password": "0000",
                                        "trig_word": 'rape'},
                                  follow_redirects=True)
        self.assertIn(b"login", result.data)

    def test_tagging_news(self):
        """Test tagging news article and adding it to the database"""
        trig_article = "This is a test triggering article."
        route = "/trig-submitted/<trig_article>/<user_id>"
        result = self.client.post(route,
                                  data={'trig_article': trig_article,
                                        "trig_words": "war",
                                        'date_added': date.today()})
        self.assertIn(b"successfully", result.data)

######################################################################
# Helper functions to run the tests
######################################################################


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    BannedNews.query.delete()

    # Add sample employees and departments
    news1 = BannedNews(trig_article='This is an example',
                       trig_words='rape, war',
                       date_added=date.today())
    news2 = BannedNews(trig_article='This is an example',
                       trig_words='assault',
                       date_added=date.today())
    news3 = BannedNews(trig_article='This is an example',
                       trig_words='rape, trump',
                       date_added=date.today())
    password = hash_password("hello")
    user1 = User(email='hello@gmail.com',
                 password=password,
                 trig='rape')
    user2 = User(email='test@gmail.com',
                 password=password,
                 trig='war')
    user3 = User(email='hi@gmail.com',
                 password=password,
                 trig='rape')

    db.session.add_all([news1, news2, news3, user1, user2, user3])
    db.session.commit()


if __name__ == '__main__':
    unittest.main()
