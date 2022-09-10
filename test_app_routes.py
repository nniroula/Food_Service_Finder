"""User Views tests."""

# run these tests like:
#
#   python -m unittest test_app_routes.py or
#   FLASK_ENV=production python -m unittest test_app_routes.py

import os
from unittest import TestCase
from models import db, User
from app import app

# Before importing the app, set an environmental variable to use a different database for testinng
os.environ['DATABASE_URL'] = "postgresql:///test_db"

from app import app

# Create our tables once for all tests - in each test, delete the data and create fresh new clean test data
db.create_all()

app.config["WTF_CSRF_ENABLED"] = False


class UserViewsTestCase(TestCase):
    """ Testing view functions for user and restaurant routes"""

    def setUp(self):
        """Create test client, add some sample data."""

        User.query.delete()

        self.client = app.test_client()

        # Create test users
        self.testUser1 = User.signup(
            firstname='John',
            lastname = 'Doe',
            username="tester1",
            password="hashedPasswordOne"
        )
        self.testUser1.id = 1

        self.testUser2 = User.signup(
            firstname='pabitra',
            lastname = 'luitel',
            username="tester2",
            password="hashedPasswordTwo",
        )
        self.testUser2.id = 2

        db.session.commit()


    def tearDown(self):
        """Clean up transactions."""

        db.session.rollback()

    def test_signup(self):
        """Check that Sign Up root route functions properly"""
        with self.client as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)


    def test_secret_route_redirects_to_home_page(self):
        """Check that private route redirect to the home page if accessed before logging in. """

        with self.client as client:
            res = client.get(f"/search")
            self.assertEqual(res.status_code, 302)


    def test_login(self):
        """Make sure that login route works as expected """

        with self.client as client:
            res = client.get('/login') 
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h4>Please login</h4>', html)


    def test_logout(self):
        """Confirm that logout route works correctly"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['current_user'] = self.testUser1.id 

            res = client.get("/logout")
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/login')


    def test_profile_route_redirects_to_home_page_before_login(self):
        """Check route for user profile before a user is logged in. """

        with self.client as client:
            res = client.get(f"/users/profile")
            self.assertEqual(res.status_code, 302)


    def test_four_o_four_route(self):
        """Check that invalid route renders 404 page. """
        with self.client as client:
            res = client.get('/invalidroute')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 404)