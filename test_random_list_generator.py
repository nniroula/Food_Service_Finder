"""Random list generator function test."""

# run these tests in your venv directory with the following command:
#
#   (venv) python -m unittest test_random_list_generator.py or
#   (venv) FLASK_ENV=production python -m unittest test_random_list_generator.py .py


from unittest import TestCase
from app import generate_random_list_of_items

class RandomListGeneratorTestCase(TestCase):
    """ Testing random list generator functions for displaying 12 random stores at maximum at a time. """

    list1 = ['JS', 'Python', 'Ruby', 'C#', 'C++', 'Elixir', 'Cobolt', 'Scala', 'Java', 'NodeJs', 'Fortran', 'Visual Basic']

    def test_random_list_generator(self):
        """ Test if two lists are equal. """

        expected = sorted(self.list1)
        actual = sorted(generate_random_list_of_items(self.list1))
        self.assertListEqual(actual, expected)


        