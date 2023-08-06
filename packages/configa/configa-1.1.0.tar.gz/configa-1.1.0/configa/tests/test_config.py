"""Unit tests for :class:`Configa`.

"""
import pytest

import configa


def test_config_init():
    """Initialise a configa.Config object.
    """
    # When I initialise a configa.Config object
    conf = configa.Config()

    # I should get a configa.Config instance
    msg = 'Object is not a configa.Config instance'
    assert isinstance(conf, configa.Config), msg


def test_parse_config_no_conf_path():
    """Read config with no file provided.
    """
    # Given a configa.Config instance
    conf = configa.Config()

    # when I attempt to parse the config without a source file defined
    received = conf.parse_config()

    # then I should receive an False alert
    msg = 'Valid config read did not return True'
    assert not received, msg


def test_parse_config(test_config_path):
    """Read valid config.
    """
    # Given a configa.Config instance
    conf = configa.Config(test_config_path)

    # when attempt to parse the config
    received = conf.parse_config()

    # then I should received a True response
    msg = 'Valid config read did not return True'
    assert received, msg


def test_parse_scalar_config(dummy_config):
    """parse_scalar_config() helper method.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a configuration section/option
    section = 'dummy_section'
    option = 'dummy_key'
    var = 'dummy_key'

    # and feed the settings into the parse_scalar_config() method
    received = dummy_config.parse_scalar_config(section, option, var)

    # then I should receive the expected section/option value
    expected = 'dummy_value'
    msg = 'Parsed config scalar error'
    assert received == expected, msg

    # ... and check that the variable is set.
    received = dummy_config.dummy_key
    msg = 'Parsed config scalar: set variable error'
    assert received == expected, msg


def test_parse_scalar_config_is_required_missing_option(dummy_config):
    """Parse required scalar from the config file: missing option.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a missing configuration section's option
    kwargs = {
        'section': 'summy_section',
        'option': 'missing_option',
        'is_required': True
    }

    # then the config parser should exit the program
    pytest.raises(SystemExit, dummy_config.parse_scalar_config, **kwargs)


def test_parse_scalar_config_is_required_missing_section(dummy_config):
    """Parse required scalar from the config file: missing section.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a missing configuration section
    kwargs = {
        'section': 'missing_section',
        'option': str(),
        'is_required': True
    }

    # then the config parser should exit the program
    pytest.raises(SystemExit, dummy_config.parse_scalar_config, **kwargs)


def test_parse_scalar_config_as_int(dummy_config):
    """Parse a scalar from the configuration file: cast to int.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a configuration section with integer value
    kwargs = {
        'section': 'int_section',
        'option': 'int_key',
        'cast_type': 'int',
    }
    received = dummy_config.parse_scalar_config(**kwargs)

    # then the config parser should return an integer value
    msg = 'Parsed config scalar error: cast to int'
    assert received == 1234, msg


def test_parse_scalar_config_no_value_found(dummy_config):
    """Parse a scalar from the configuration file: no value found.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a configuration section with no value
    kwargs = {
        'section': 'dummy_setion',
        'option': 'empty_key',
        'var': 'empty_key',
    }
    received = dummy_config.parse_scalar_config(**kwargs)

    # then the config scalar parser should return None
    msg = 'Parsed config scalar error: no value found/no var'
    assert not received, msg


def test_parse_scalar_config_as_list(dummy_config):
    """Parse a scalar from the configuration file: as list.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a configuration section with a list-based value
    kwargs = {
        'section': 'dummy_section',
        'option': 'dummy_list',
        'var': 'dummy_list',
        'is_list': True,
    }
    received = dummy_config.parse_scalar_config(**kwargs)

    # then the config scalar parser should return a list
    expected = ['list 1', 'list 2']
    msg = 'Parsed config scalar error: lists'
    assert received == expected, msg


def test_parse_dict_config(dummy_config):
    """Parse a dict (section) from the configuration file.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a dictionary-based configuration section
    received = dummy_config.parse_dict_config(section='dummy_dict_section')

    # then I should receive a dictionary
    expected = {'dict_1': 'dict 1 value', 'dict_2': 'dict 2 value'}
    msg = 'Parsed config dict error'
    assert received == expected, msg


def test_parse_dict_config_is_required(dummy_config):
    """Parse a required dict (section) from the configuration file.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a missing dictionary-based configuration section that is required
    kwargs = {
        'section': 'missing_dict_section',
        'is_required': True
    }

    # then the config parser should exit the program
    pytest.raises(SystemExit, dummy_config.parse_dict_config, **kwargs)


def test_parse_dict_config_as_int(dummy_config):
    """Parse a dict (section) from the configuration file (as int).
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a dictionary-based integer configuration section
    kwargs = {
        'section': 'dummy_dict_int',
        'cast_type': 'int'
    }
    received = dummy_config.parse_dict_config(**kwargs)

    # then the config dictionary parser should return integer values
    expected = {'dict_1': 1234}
    msg = 'Parsed config dict as int error'
    assert received == expected, msg


def test_parse_dict_config_key_as_int(dummy_config):
    """Parse a dict (section) from the configuration file (key as int).
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a dictionary-based integer key configuration section
    kwargs = {
        'section': 'dummy_dict_key_as_int',
        'key_cast_type': 'int',
    }
    received = dummy_config.parse_dict_config(**kwargs)

    # then I should receive a dictionary whose keys are integers
    expected = {1234: 'int_key_value'}
    msg = 'Parsed config dict with key as int error'
    assert received == expected, msg


def test_parse_dict_config_key_upper_case(dummy_config):
    """Parse a dict (section) from the configuration file (key upper).
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a dictionary-based upper-case key configuration
    # section
    kwargs = {
        'section': 'dummy_dict_key_as_upper',
        'key_case': 'upper',
    }
    received = dummy_config.parse_dict_config(**kwargs)

    # then I should receive a dictionary whose keys are all upper-case
    expected = {'ABC': 'upper_key_value'}
    msg = 'Parsed config dict (key upper case) error'
    assert received == expected, msg


def test_parse_dict_config_key_lower_case(dummy_config):
    """Parse a dict (section) from the configuration file (key lower).
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a dictionary-based lower-case key configuration
    # section
    kwargs = {
        'section': 'dummy_dict_key_as_lower',
        'key_case': 'lower',
    }
    received = dummy_config.parse_dict_config(**kwargs)

    # then I should receive a dictionary whose keys are all lower-case
    expected = {'abc': 'lower_key_value'}
    msg = 'Parsed config dict (key lower case) error'
    assert received == expected, msg


def test_parse_dict_config_list_values(dummy_config):
    """Parse a dict (section) from the configuration file: list values.
    """
    # Given a configa.Config instance with a valid path to a configuration file

    # when I target a dictionary-based key configuration
    # section whose values are a list
    kwargs = {
        'section': 'dummy_dict_as_list',
        'is_list': 'True',
    }
    received = dummy_config.parse_dict_config(**kwargs)

    # then I should receive a dictionary whose keys are all lower-case
    expected = {
        'dict_1': [
            'list item 1',
            'list item 2'
        ],
        'dict_2': [
            'list item 3',
            'list item 4'
        ]
    }
    msg = 'Parsed config dict error (as list)'
    assert received == expected, msg

    # and the instance variable should be set
    received = dummy_config.dummy_dict_as_list
    msg = 'Parsed config dict set variable error (as list)'
    assert received == expected, msg
