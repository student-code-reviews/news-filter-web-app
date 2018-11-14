import project_server
from unittest import TestCase
from project_server import app


# class MyAppUnitTestCase(TestCase):

#     def test_

######################################################################
# Tests that don't require the database nor an active session
######################################################################

class FlaskTests(TestCase):

    def setUp(self):
        """ Stuff to do before every test. """

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
        self.assertIn(b"Login here: ", result.data)

    def test_register_page(self):
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h2>Email address:</h2>", result.data)


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

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        connect_to_db(app, "postgresql:///testdb")

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'k@gmail.com'

    def test_important_page(self):
        """Test important page."""

        result = self.client.get("/important")
        self.assertIn(b"You are a valued user", result.data)

######################################################################
# Tests that require an active session, but no database access
######################################################################

    def test_homepage_session(self):
        """ Test homepage when user is logged in."""
        result = self.client.get("/")


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'k@gmail.com'

    def test_important_page(self):
        """Test important page."""

        result = self.client.get("/important")
        self.assertIn(b"You are a valued user", result.data)


if __name__ == '__main__':
    unittest.main()
