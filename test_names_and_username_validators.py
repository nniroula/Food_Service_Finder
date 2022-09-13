"""Tests for first name, last name, and username validator fucntions."""

from unittest import TestCase
from app import alphabetic_name, alphanumeric_username

class FirstLastNamesAndUsernameTestCase(TestCase):
    """ Tests for first, last, and username validators. """
    
    def test_first_name_field_empty(self):
        """ Empty first name field should return false. """

        firstname = ''
        self.assertFalse(alphabetic_name(firstname))


    def test_first_name_not_text(self):
        """ Non-text first name should return false. """

        firstname = '123@#'
        self.assertFalse(alphabetic_name(firstname))

    
    def test_valid_firstname_field(self):
        """ alphabetic name function should return true if the first name is valid"""

        firstname = 'John'
        self.assertTrue(alphabetic_name(firstname))


    def test_empty_username_field(self):
        """ Empty user name field should return false. """

        username = ''
        self.assertFalse(alphanumeric_username(username))

    
    def test_invalid_username_field(self):
        """ Non-alphanumeric username field should return false. """

        username = 'a1!@#$'
        self.assertFalse(alphanumeric_username(username))


    def test_valid_username(self):
        """ Alphanumeric username should return True. """

        username = 'n86'
        self.assertTrue(alphanumeric_username(username))



   


        