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
    list2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    list3 = [1, 2, 3, 4, 5]
    

    def test_random_list_generator(self):
        """ Test if two lists are equal. """

        expected = sorted(self.list1)
        actual = sorted(generate_random_list_of_items(self.list1))
        self.assertListEqual(actual, expected)


    def test_length_of_resultant_list_after_random_generation_is_twelve(self):
        """ check if the length of the resultant list after passing a list with length greater than 12 through a 
        random list generator function is 12. """

        actual = generate_random_list_of_items(self.list2)
        self.assertEqual(len(actual), 12)


    def test_less_than_12_items(self):
        """ chekc if the random list generator works correctly if lenght of an array is less than 12. """

        expected = sorted(self.list3)
        actual = sorted(generate_random_list_of_items(self.list3))
        self.assertListEqual(actual, expected)


        