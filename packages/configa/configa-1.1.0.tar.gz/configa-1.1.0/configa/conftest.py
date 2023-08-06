"""Global fixture arrangement at the `configa` package level.

"""
import os
import logging as log
import pytest

import configa
import configa.setter


@pytest.fixture(scope='module')
def test_config_path():
    """Path to test configuration.
    """
    dirpath = os.path.join('configa', 'tests', 'files', 'dummy.conf')
    log.info('Test config directory: "%s"', dirpath)

    return dirpath


@pytest.fixture(scope='function')
def dummy_config(test_config_path):
    """Re-usable Dummy Config instance.
    """
    class DummyConfig(configa.Config):
        """Dummy class for testing config.

        """
        def __init__(self, conf_filepath):
            configa.Config.__init__(self, conf_filepath)

            self.__dummy_key = None
            self.__int_key = None
            self.__empty_key = None
            self.__dummy_list = []
            self.__dummy_dict_section = {}
            self.__dummy_dict_int = {}
            self.__dummy_dict_key_as_int = {}
            self.__dummy_dict_key_as_upper = {}
            self.__dummy_dict_key_as_lower = {}
            self.__dummy_dict_as_list = {}

        @property
        def dummy_key(self):
            """:attr:`dummy_key` getter.
            """
            return self.__dummy_key

        @configa.setter.set_scalar
        def set_dummy_key(self, value):
            """:attr:`dummy_key` setter.
            """

        @property
        def int_key(self):
            """:attr:`int_key` getter.
            """
            return self.__int_key

        @configa.setter.set_scalar
        def set_int_key(self, value):
            """:attr:`int_key` setter.
            """

        @property
        def empty_key(self):
            """:attr:`empty_key` getter.
            """
            return self.__empty_key

        @configa.setter.set_scalar
        def set_empty_key(self, value):
            """:attr:`empty_key` setter.
            """

        @property
        def dummy_list(self):
            """:attr:`dummy_list` getter.
            """
            return self.__dummy_list

        @configa.setter.set_list
        def set_dummy_list(self, value):
            """:attr:`dummy_list` setter.
            """

        @property
        def dummy_dict_section(self):
            """:attr:`dummy_dict_section` getter.
            """
            return self.__dummy_dict_section

        @configa.setter.set_dict
        def set_dummy_dict_section(self, value):
            """:attr:`dummy_dict_section` setter.
            """

        @property
        def dummy_dict_int(self):
            """:attr:`dummy_dict_int` getter.
            """
            return self.__dummy_dict_int

        @configa.setter.set_dict
        def set_dummy_dict_int(self, value):
            """:attr:`dummy_dict_int` setter.
            """

        @property
        def dummy_dict_key_as_int(self):
            """:attr:`dummy_dict_key_as_int` getter.
            """
            return self.__dummy_dict_key_as_int

        @configa.setter.set_dict
        def set_dummy_dict_key_as_int(self, value):
            """:attr:`dummy_dict_key_as_int` getter.
            """

        @property
        def dummy_dict_key_as_upper(self):
            """:attr:`dummy_dict_key_as_upper` getter.
            """
            return self.__dummy_dict_key_as_upper

        @configa.setter.set_dict
        def set_dummy_dict_key_as_upper(self, value):
            """:attr:`dummy_dict_key_as_upper` setter.
            """

        @property
        def dummy_dict_key_as_lower(self):
            """:attr:`dummy_dict_key_as_lower` getter.
            """
            return self.__dummy_dict_key_as_lower

        @configa.setter.set_dict
        def set_dummy_dict_key_as_lower(self, value):
            """:attr:`dummy_dict_key_as_lower` setter.
            """

        @property
        def dummy_dict_as_list(self):
            """:attr:`dummy_dict_key_as_list` getter.
            """
            return self.__dummy_dict_as_list

        @configa.setter.set_dict
        def set_dummy_dict_as_list(self, value):
            """:attr:`dummy_dict_key_as_list` setter.
            """

    return DummyConfig(test_config_path)
