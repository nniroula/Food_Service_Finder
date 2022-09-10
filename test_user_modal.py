"""User model tests."""

# run these tests like:
# In your venv folder, run following command
#  (venv)$ python -m unittest test_user_modal.py or 
#  (venv)$ FLASK_ENV=production python -m unittest test_user_model.py


import os
from unittest import TestCase
from app import app

from models import db, User

# from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///test_db"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


db.create_all()


class UserModelTestCase(TestCase):
    """Test User modal """

    def setUp(self):
        """Create test client, and add some sample data."""

        # clean up existing users
        User.query.delete()

        self.client = app.test_client()

        self.testUser1 = User.signup(
            firstname='John',
            lastname = 'Doe',
            username="one",
            password="one123"
        )
        self.testUser1.id = 1

        self.testUser2 = User.signup(
            firstname='pabitra',
            lastname = 'luitel',
            username="tester2",
            password="hashedPasswordTwo",
        )
        self.testUser2.id = 2

        db.session.add(self.testUser1)
        db.session.add(self.testUser2)
        db.session.commit()
    

    def test_does_user_model_work(self):
        """Does basic model work?"""

        user_in_User_modal = User(
           firstname='prinsu',
            lastname = 'niroula',
            username="modaltester1",
            password="hashed",
        )

        db.session.add(user_in_User_modal)
        db.session.commit()

        self.assertTrue(user_in_User_modal)


    def test__repr__(self):
        """Does the repr method work as expected?"""

        response = self.testUser1.__repr__()
        self.assertEqual(response, f"<User #{self.testUser1.id}: {self.testUser1.username}>")
      

    def test_is_user_signedup_successfully(self):
        """ Is a user created successfully given valid credentials? """

        user = User.query.get(2)
        self.assertEqual(user, self.testUser2)


    def test_does_user_signup_fail_with_invalid_password(self): 
        """ Check if sign up fails with invalid password. """

        with self.assertRaises(ValueError):
            self.assertIsNotNone(User.signup("firstNameHere", "lasteNameHere", 'usernameHere', None))


    def test_does_user_signup_fail_with_invalid_username(self):
        """ Check if user sign up fail with invalid username. """

        with self.assertRaises(ValueError):
            self.assertIsNotNone(User.signup("firstNameHere", "lasteNameHere", None, None))


