import project_server
from unittest import TestCase
from project_server import app
from six import b


# class MyAppUnitTestCase(TestCase):

#     def test_

######################################################################
# Tests that don't require the database nor an active session.
# Summary of tests in this section: homepage, log in page,
# register page.
######################################################################

class FlaskTests(TestCase):

    def setUp(self):
        """ Stuff to do before every test. """

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        """ Stuff to do after each test."""
        pass

    def test_homepage(self):
        """ Test homepage when user is not logged in."""
        result = self.clent.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Filtered News</h1>', result.data)

    def test_login_page(self):
        """ Test whether login page is displayed. """
        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2>Login here: </h2>', result.data)

    def test_login(self):
        """Test whether user can login."""

        result = self.client.post("/login",
                                  data={"email": "k@gmail.com", "password": "123"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2>Login here: </h2>', result.data)

    def test_register_page(self):
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h2>Email address:</h2>", result.data)


######################################################################
# Tests that require an active session, but no database access
######################################################################

class FlaskTestsSessionOn(TestCase):
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
        self.assertIn("Logged out!", result.data)


######################################################################
# Tests that require database access and an active session, but don't
# alter the state of the database.
######################################################################

class FlaskTestsLoggedIn(TestCase):
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
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'k@gmail.com'

    def tearDown(self):
        """Do at the end of every test"""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """ Tests if login function works and
        is able to access database."""

        result = self.client.post("/logged-in",
                                  data={"email": 'hello@gmail.com',
                                        "password": '010101'},
                                  follow_redirects=True)

        self.assertIn("You have successfully logged in!", result.data)

# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'ABC'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user'] = 'k@gmail.com'

######################################################################
# Tests that require database access, need an active session, and
# can actually change the database.
######################################################################

######################################################################
# Helper functions to run the tests
######################################################################


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
    news2 = BannedNews(news_id=2,
                       trig_article='This is an examle',
                       trig_words='assault',
                       date_added=date.today())
    news3 = BannedNews(news_id=3,
                       trig_article='This is an examle',
                       trig_words='rape, trump',
                       date_added=date.today())

    user1 = User(user_id=1,
                 email='hello@gmail.com',
                 password='010101',
                 trig='rape')
    user2 = User(user_id=2,
                 email='test@gmail.com',
                 password='010101',
                 trig='war')
    user3 = User(user_id=3,
                 email='hi@gmail.com',
                 password='010101',
                 trig='rape')

    db.session.add_all([news1, news2, news3, user1, user2, user3])
    db.session.commit()


if __name__ == '__main__':
    unittest.main()
