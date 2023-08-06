""":mod:`configa.setter` tests.

"""
import unittest
import datetime

from configa.setter import (set_scalar,
                            set_date,
                            set_tuple,
                            set_list,
                            set_dict)


class Bogus(object):
    """Bogus class definition for testing purposes.

    """
    def __init__(self):
        self.__bogus_scalar = None
        self.__bogus_date = None
        self.__bogus_tuple = ()
        self.__bogus_list = []
        self.__bogus_dict = {}

    @property
    def bogus_scalar(self):
        return self.__bogus_scalar

    @set_scalar
    def set_bogus_scalar(self, value):
        pass

    @property
    def bogus_date(self):
        return self.__bogus_date

    @set_date
    def set_bogus_date(self, value):
        pass

    @property
    def bogus_tuple(self):
        return self.__bogus_tuple

    @set_tuple
    def set_bogus_tuple(self, value):
        pass

    @property
    def bogus_list(self):
        return self.__bogus_list

    @set_list
    def set_bogus_list(self, values):
        pass

    @property
    def bogus_dict(self):
        return self.__bogus_dict

    @set_dict
    def set_bogus_dict(self, values):
        pass

    @set_scalar
    def set_missing_attr(self, value):
        pass

    def __str__(self):
        return self.__class__.__name__


class TestSetter(unittest.TestCase):

    def test_set_scalar(self):
        """Set a scalar value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a scalar value via the setter
        value = 'Bogus Value'
        bogus.set_bogus_scalar(value)

        # then the Bogus instance scalar attribute should be set
        received = bogus.bogus_scalar
        expected = value
        msg = 'Attribute bogus_scalar set error'
        self.assertEqual(received, expected, msg)

    def test_set_date(self):
        """Set a date value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a date value via the setter
        value = '2013-10-09 00:00:00'
        bogus.set_bogus_date(value)

        # then the Bogus instance date attribute should be set
        received = bogus.bogus_date
        expected = datetime.datetime(2013, 10, 9, 0, 0)
        msg = 'Attribute bogus_scalar set error'
        self.assertEqual(received, expected, msg)

    def test_set_date_with_real_dt(self):
        """Set a date value (datetime object).
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a datetime object value via the setter
        value = datetime.datetime(2004, 2, 12, 0, 0)
        bogus.set_bogus_date(value)

        # then the Bogus instance date attribute should be set
        received = bogus.bogus_date
        expected = datetime.datetime(2004, 2, 12, 0, 0)
        msg = 'Attribute bogus_scalar set error'
        self.assertEqual(received, expected, msg)

    def test_set_tuple(self):
        """Set a tuple value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a tuple object value via the setter
        values = ('tuple item 1', 'tuple item 2')
        bogus.set_bogus_tuple(values)

        # then the Bogus instance tuple attribute should be set
        received = bogus.bogus_tuple
        expected = values
        msg = 'Attribute bogus_tuple set error'
        self.assertTupleEqual(received, expected, msg)

        # and if I set a new set of tuple values
        values = ('tuple item 3', 'tuple item 4')
        bogus.set_bogus_tuple(values)

        # then the Bogus instance tuple attribute should be clobberred
        received = bogus.bogus_tuple
        expected = values
        msg = 'Attribute bogus_tuple set error'
        self.assertTupleEqual(received, expected, msg)

    def test_set_list(self):
        """Set a list value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a list object value via the setter
        values = ['list item 1', 'list item 2']
        bogus.set_bogus_list(values)

        # then the Bogus instance list attribute should be set
        received = bogus.bogus_list
        expected = values
        msg = 'Attribute bogus_scalar set error'
        self.assertListEqual(sorted(received), sorted(expected), msg)

        # and if I set a new set of tuple values
        values = ['list item 3', 'list item 4']
        bogus.set_bogus_list(values)

        # then the Bogus instance list attribute should be clobberred
        received = bogus.bogus_list
        expected = values
        msg = 'Attribute bogus_list set error'
        self.assertListEqual(sorted(received), sorted(expected), msg)

    def test_set_list_with_none(self):
        """Set a list value: None value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a None value via the list attribute setter
        values = None
        bogus.set_bogus_list(values)

        # then the Bogus instance list attribute should be an empty list
        received = bogus.bogus_list
        expected = []
        msg = 'Attribute bogus_list (None value) set error'
        self.assertListEqual(sorted(received), sorted(expected), msg)

    def test_set_dict_with_none(self):
        """Set a dict value: None value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a None value via the dictionary attribute setter
        values = None
        bogus.set_bogus_dict(values)

        # then the Bogus instance dict attribute should be an empty dict
        received = bogus.bogus_dict
        expected = {}
        msg = 'Attribute bogus_dict (None value) set error'
        self.assertDictEqual(received, expected, msg)

    def test_set_dict(self):
        """Set a dict value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a dictionary via the dictionary attribute setter
        values = {
            'dict item 1': 1,
            'dict item 2': 2
        }
        bogus.set_bogus_dict(values)

        # then the Bogus instance dict attribute should be a populated dict
        received = bogus.bogus_dict
        expected = values
        msg = 'Attribute bogus_scalar set error'
        self.assertDictEqual(received, expected, msg)

        # and if I set a new set of dict values
        values = {
            'dict item 3': 3,
            'dict item 4': 4
        }
        bogus.set_bogus_dict(values)

        # then the Bogus instance dict attribute should be clobberred
        received = bogus.bogus_dict
        expected = values
        msg = 'Attribute bogus_dict set error'
        self.assertDictEqual(received, expected, msg)

    def test_set_scalar_missing_attr(self):
        """Set a scalar value: missing attribute.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a scalar value to an undefined Bogus attribute
        value = 'Bogus Value'

        # then the class instance should throw an exception
        err_msg = "'Bogus' object has no attribute '_Bogus__missing_attr'"
        self.assertRaisesRegex(AttributeError,
                               err_msg,
                               bogus.set_missing_attr,
                               value)

    def test_set_scalar_non_scalar_value(self):
        """Set a scalar value: non scalar value.
        """
        # Given a Bogus() instance
        bogus = Bogus()

        # when I provide a list value to an class instance attribute
        value = ['Bogus Value']

        # then the class instance should throw an exception
        self.assertRaisesRegex(TypeError,
                               '"\[\'Bogus Value\']" is not a scalar',
                               bogus.set_bogus_scalar,
                               value)

        # and check the class instance attribute should remain unchanged.
        received = bogus.bogus_scalar
        msg = 'Attribute bogus_scalar set error'
        self.assertIsNone(received, msg)
