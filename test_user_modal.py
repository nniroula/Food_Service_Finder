"""User model tests."""

# run these tests like:
# In your venv folder, run following command
#  (venv)$ python -m unittest test_user_modal.py or 
#  (venv)$ FLASK_ENV=production python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User

# from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///project_test_db"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add some sample data."""

        User.query.delete()
        # Message.query.delete()


        self.client = app.test_client()

      # Create Users
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

# ASK 0, Do I need to do this to run #Ask 2
        # save in database
        db.session.add(self.testUser1)
        db.session.add(self.testUser2)
        db.session.commit()


    # ################################

    # tests

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

# ASK 1
        # self.assertEqual(len(user_in_User_modal.users), 1)
        # self.assertEqual(len(user_in_User_modal.), 1)

        self.assertTrue(user_in_User_modal)


    def test__repr__(self):
        """Does the repr method work as expected?"""

        response = self.testUser1.__repr__()

        self.assertEqual(response, f"<User #{self.testUser1.id}: {self.testUser1.username}>")
        # return f"<User #{self.id}: {self.username}>"


# Ask 2
    def test_is_user_created_successfully(self):
        """Does User.create successfully create a new user given valid credentials?"""
        # User.create is signup
        user = User.query.get(2)
        self.assertEqual(user, self.testUser2)
    
# ASK 3, it keeps failing AssertionError: ValueError not raised
    def test_does_user_signup_fail_with_invalid_password(self): #length >= 6
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        # login with invalid password
        with self.assertRaises(ValueError):
            # User.signup("username", "lastNameHere", 'testUser1', None)
            User.signup("firstNameHere", "lastNameHere", 'username1', '')


# ASK 4 AssertionError: ValueError not raised
    def test_does_user_signup_fail_with_invalid_username(self):
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        with self.assertRaises(ValueError):
            User.signup("firstNameHere", "lasteNameHere", None, "passwordHere")

    

    def test_authenticate(self):
        """ Does User.authenticate successfully return a user when given a valid username and password?"""
       
        generate_hash_password = bcrypt.generate_password_hash(self.testUser1.password).decode('UTF-8')
        pword_hash_Check = bcrypt.check_password_hash(generate_hash_password, self.testUser1.password)

        user = User.query.get(self.testUser1.id)
        authenticated_user = User.authenticate(self.testUser1.username, "hashedPasswordOne")
       
        self.assertTrue(pword_hash_Check)
        self.assertIsNotNone(authenticated_user)  # make sure user exists by checking it is NOT NONE
        self.assertEqual(user, authenticated_user)


    def test_authetication_fails_with_invalid_username(self):
        """ Does User.authenticate fail to return a user when the username is invalid?"""
        self.assertFalse(User.authenticate("invalidusername", "invalidpassword")) # OR
        self.assertEqual(User.authenticate("invalidusername", "invalidpassword"), False)

    
    def test_authetication_fails_with_invalid_password(self):
        """ Does User.authenticate fail to return a user when the password is invalid?"""
        self.assertEqual(User.authenticate(self.testUser1 .username, "invalidpassword"), False)
