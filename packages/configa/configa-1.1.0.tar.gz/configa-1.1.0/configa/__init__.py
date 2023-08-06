""":class:`Config`.

"""
import sys
import builtins
import os
import configparser
import logging as log

ROOT = log.getLogger()
ROOT.setLevel(log.INFO)

if not ROOT.hasHandlers():
    HANDLER = log.StreamHandler(sys.stdout)
    HANDLER.setLevel(log.INFO)
    FORMATTER = log.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    HANDLER.setFormatter(FORMATTER)
    ROOT.addHandler(HANDLER)

__all__ = ["Config"]


class Config(configparser.ConfigParser):
    """:class:`configa.Config` class.

    .. attribute:: *config_filepath*

        path to the configuration file to parse

    .. note::

        The :class:`Config` class inherits from the old-style
        :class:`configparser.ConfigParser` and does not support
        property getters and setters.

    """
    def __init__(self, config_file=None):
        """:class:`configa.Config` initialisation.

        """
        configparser.ConfigParser.__init__(self)

        self.__config_filepath = config_file

        if config_file is not None:
            self.parse_config()

    @property
    def config_filepath(self):
        """:attr:`config_filepath` getter
        """
        return self.__config_filepath

    @config_filepath.setter
    def config_filepath(self, value):
        """:attr:`config_filepath` setter
        """
        log.info('### %s', value)
        self.__config_filepath = value

    @property
    def facility(self):
        return self.__class__.__name__

    def parse_config(self):
        """Attempt to read the contents of the :attr:`configa.Config`
        (unless ``None``).

        File contents should be as per :mod:`configparser` format.

        **Returns:**
            Boolean ``True`` upon success.  Boolean ``False`` otherwise.

        """
        log.debug('Parsing config file: "%s"', self.config_filepath)
        config_parse_status = False

        if (self.config_filepath is None or
                not os.path.exists(self.config_filepath)):
            log.error('Invalid config file: "%s"', self.config_filepath)
        else:
            self.read(self.config_filepath)
            config_parse_status = True

        return config_parse_status

    def parse_scalar_config(self,
                            section,
                            option,
                            var=None,
                            cast_type=None,
                            is_list=False,
                            is_required=False):
        """Helper method that can parse a scalar value based on
        *section* and *option* in the :mod:`configparser` based
        configuration file and set *var* attribute with the value parsed.

        If *is_required* is set and configuration section/option is missing
        then the process will exit.

        **Args:**
            *section*: the configuration file section.  For example
            ``[environment]``

            *option*: the configuration file section's options to
            parse.

        **Kwargs:**
            *var*: the target attribute name.  This can be omitted if
            the target attribute name is the same as *option*

            *cast_type*: cast the value parsed as *cast_type*.  If
            ``None`` is specified, then parse as a string

            *is_list*: boolean flag to indicate whether to parse the
            option values as a list (default ``False``)

            *is_required*: boolean flag to indicate whether the
            value is required.

        **Returns:**
            the value of the scalar option value parsed

        """
        value = None

        if var is None:
            var = option

        try:
            value = self.get(section, option)
            if cast_type is not None:
                caster = getattr(builtins, cast_type)
                value = caster(value)
            if is_list:
                value = value.split(',')
            setter = getattr(self, 'set_%s' % var)
            setter(value)
        except (configparser.NoOptionError,
                configparser.NoSectionError) as err:
            if is_required:
                log.critical('Missing required config: %s', err)
                sys.exit(1)

            try:
                getter = getattr(self, var)
                msg = ('%s %s.%s not defined. Using' %
                       (self.facility, section, option))
                if isinstance(getter, (int, float, complex)):
                    log.debug('%s %d', msg, getter)
                else:
                    log.debug('%s "%s"', msg, getter)
            except AttributeError as err:
                log.debug('%s %s.%s not defined: %s',
                          self.facility, section, option, err)

        return value

    def parse_dict_config(self,
                          section,
                          var=None,
                          cast_type=None,
                          key_cast_type=None,
                          key_case=None,
                          is_list=False,
                          is_required=False):
        """Helper method that can parse a :mod:`configparser` *section*
        and set the *var* attribute with the value parsed.

        :mod:`configparser` sections will produce a dictionary structure.
        If *is_list* is ``True`` the section's options values will be
        treated as a list.  This will produce a dictionary of lists.

        **Args:**
            *section*: the configuration file section.  For example
            ``[comms_delivery_partners]``

        **Kwargs:**
            *var*: the target attribute name.  This can be omitted if
            the target attribute name is the same as *option*

            *cast_type*: cast the value parsed as *cast_type*.  If
            ``None`` is specified, then parse as a string

            *key_cast_type*: cast the option parsed as *cast_type*

            *key_case*: for strings, change the case of the option value

            *is_list*: boolean flag to indicate whether to parse the
            option values as a list (default ``False``)

            *is_required*: boolean flag to indicate whether the
            value is required.

        **Returns:**
            the value of the :mod:`configparser` section as a dict
            structure

        """
        value = None

        if var is None:
            var = section

        try:
            key_caster = None
            if key_cast_type is not None:
                key_caster = getattr(builtins, key_cast_type)

            tmp_value = {}
            for k, val in dict(self.items(section)).items():
                # Cast the dictionay key if required.
                key = k
                if key_caster is not None:
                    key = key_caster(k)

                if key_case == 'upper':
                    tmp_value[key.upper()] = val
                elif key_case == 'lower':
                    tmp_value[key.lower()] = val
                else:
                    tmp_value[key] = val

            # Now, take care of list values.
            if is_list:
                for k, val in tmp_value.items():
                    tmp_value[k] = val.split(',')

            # Finally, cast the value if required.
            if cast_type is not None:
                caster = getattr(builtins, cast_type)
                for k, val in tmp_value.items():
                    if isinstance(val, (list)):
                        tmp_value[k] = [caster(x) for x in val]
                    else:
                        tmp_value[k] = caster(val)

            value = tmp_value
            setter = getattr(self, 'set_%s' % var)
            setter(value)
        except (configparser.NoOptionError,
                configparser.NoSectionError) as err:
            if is_required:
                log.critical('Missing required config: %s', err)
                sys.exit(1)

            try:
                getter = getattr(self, var)
                msg = ('%s %s not defined.  Using' %
                       (self.facility, section))
                if isinstance(getter, (int, float, complex)):
                    log.debug('%s %d', msg, getter)
                else:
                    log.debug('%s "%s"', msg, getter)
            except AttributeError as err:
                log.debug('%s %s not defined: %s.',
                          self.facility, section, err)

        return value
