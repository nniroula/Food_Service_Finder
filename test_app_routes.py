"""User Views tests."""

# run these tests like:
#
#   python -m unittest test_integration_routes.py or
#   FLASK_ENV=production python -m unittest test_integration_routes.py

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

        self.testUser3 = User.signup(
            firstname='prabha',
            lastname = 'niroula',
            username="tester3",
            password="hashedPasswordThree",
        )
        self.testUser3.id = 3

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
            # self.assertIn("Name of Restaurant", html)


# ASK 5 how to get restaurant id
    def test_show_restaurant_details(self):
        """Check route for restaurant details"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['current_user'] = self.testUser1.id

            # res = client.get("/logout")
            # self.assertEqual(res.status_code, 302)
            # self.assertEqual(res.location, 'http://localhost/login')

        # with self.client as client:
        #     # res = client.get(f"/restaurant/{self.restaurant.id}")
        #     res = client.get(f"/restaurant/{restaurant.id}")
        #     self.assertEqual(res.status_code, 200)
            # self.assertIn("Name of Restaurant", str(res.data))

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


    # def test_route_for_retrieving_restaurants_from_api(self):
    #     """Check route for following another user """

    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u1.id

    #         res = client.get(f"/users/{self.u1_id}/followers")
    #         self.assertEqual(res.status_code, 200)
    #         self.assertIn("@TestUsername1", str(res.data))

    #     # user not in session
    #     with self.client as client:
    #         res = client.get(f"users/{self.u1_id}/followers")
    #         self.assertLessEqual(res.status_code, 302)
    #         self.assertIn("@TestUsername1", str(res.data))


    # def test_show_user_following(self):
    #     """Check route for following another user """

    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u1.id

    #         res = client.get(f"/users/{self.u1_id}/followers")
    #         self.assertEqual(res.status_code, 200)
    #         self.assertIn("@TestUsername1", str(res.data))

    #     # user not in session
    #     with self.client as client:
    #         res = client.get(f"users/{self.u1_id}/followers")
    #         self.assertLessEqual(res.status_code, 302)
    #         self.assertIn("@TestUsername1", str(res.data))



    # def test_show_add_like(self):
    #     """Test a route when a message is liked"""
    #     with self.client as client:
    #         id = self.msg.id
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u1.id

    #         res = client.post(f"/users/like/{id}", follow_redirects=True)
    #         self.assertEqual(res.status_code, 200)

    # def test_show_remove_like(self):
    #     """Test a route when a message is disliked"""
     
    #     msg = Message.query.filter(Message.text=="Test Message").one()  # Get message from Database
    #     self.assertIsNotNone(msg)
    #     self.assertNotEqual(msg.user_id, self.u1_id)

    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u1_id

    #         resp = client.post(f"/users/like/{msg.id}", follow_redirects=True)
    #         self.assertEqual(resp.status_code, 200)