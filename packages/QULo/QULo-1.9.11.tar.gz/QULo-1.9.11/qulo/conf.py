#!/bin/env python

#######################################################################
# Copyright (C) 2018, 2019 David Palao
#
# This file is part of QULo.
#
#  QULo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  QULo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with QULo.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import sys
import os
import argparse
import configparser

from qulo.logs import setup_logging
from qulo.sensors import sensor_factory

from qulo.constants import (
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE, ACTION_STR, ACTION_HELP, ACTION_CHOICES,
    PIDFILE_OPTION_ALIASES, PIDFILE_HELP, PIDFILE_STR,
    QULOD_PROGRAM, QULOD_DESCRIPTION, QULOD_DEFAULT_CONFIGFILE, 
    QAGENT_PROGRAM, QAGENT_DESCRIPTION, QAGENT_DEFAULT_CONFIGFILE,
    CONFIGFILE_STR, CONF_READ_MSG, PROTO_INVALID_SENSOR_MSG,
    QMASTER_PROGRAM, QMASTER_DESCRIPTION, QMASTER_DEFAULT_CONFIGFILE,
    QMASTER_HOST, QMASTER_HOST_KEY,
    QAGENT_TO_QMASTER_DATA_PORT, QAGENT_TO_QMASTER_DATA_PORT_KEY,
    GRAPHITE_HOST, GRAPHITE_HOST_KEY, GRAPHITE_CARBON_RECEIVER_PICKLE_PORT,
    GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY, GRAPHITE_SECTION,
    OWN_LOG_FILE_KEY, DEFAULT_OWN_FILE_LOGGING_PATH,
    OWN_LOG_LEVEL_KEY, DEFAULT_OWN_FILE_LOGGER_LEVEL,
    OWN_LOG_MAXBYTES_KEY, OWN_LOG_SECTION, OWN_LOG_BACKUPCOUNT_KEY,
    CONFIGFILE_STR, CONFIGFILE_OPTION_ALIASES, CONFIGFILE_HELP, 
)

ACTION_ARGUMENT = (
    ACTION_STR,
    ((ACTION_STR,), dict(help=ACTION_HELP, choices=ACTION_CHOICES)),
)

# next two should go to qulod and qagent (or constants?):
QULOD_DEFAULT_PIDFILE = os.path.join(
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE.format(program=QULOD_PROGRAM)
)
QAGENT_DEFAULT_PIDFILE = os.path.join(
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE.format(program=QAGENT_PROGRAM)
)
QMASTER_DEFAULT_PIDFILE = os.path.join(
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE.format(program=QMASTER_PROGRAM)
)

PIDFILE_ARGUMENT = (
    PIDFILE_STR,
    (PIDFILE_OPTION_ALIASES, dict(help=PIDFILE_HELP, dest=PIDFILE_STR))
)

CONFIGFILE_ARGUMENT = (
    CONFIGFILE_STR,
    (CONFIGFILE_OPTION_ALIASES, dict(help=CONFIGFILE_HELP, dest=CONFIGFILE_STR))
)


class QuloDConf:
    description = QULOD_DESCRIPTION
    default_values = {
        PIDFILE_STR: QULOD_DEFAULT_PIDFILE,
        CONFIGFILE_STR: QULOD_DEFAULT_CONFIGFILE
    }
    
    def __init__(self, argv=None):
        self._set_argv(argv)
        self._get_conf_from_command_line()
        self._set_config_file()
        self._get_conf_from_config_file()
        self._prepare_logging()
        self._post_process_configuration()

    def _set_argv(self, argv):
        if argv is None:
            argv = sys.argv[1:]
        self._argv = argv

    def _get_conf_from_command_line(self):
        self._create_cl_parser()
        self._add_arguments()
        self._parse_arguments()

    def _set_config_file(self):
        self._config_file = self[CONFIGFILE_STR]#self.default_values[CONFIGFILE_STR]
    
    def _get_conf_from_config_file(self):
        self._create_config_parser()
        self._parse_config_file()

    def _prepare_logging(self):
        self._logging_from_config_file()
        self.logger = setup_logging(
            logger_name=self.__class__.__name__,
            rotatingfile_conf=self.logging
        )
    
    def _create_config_parser(self):
        self._config_file_conf = configparser.ConfigParser()

    def _parse_config_file(self):
        self._config_file_conf.read(self._config_file)

    def _post_process_configuration(self):
        """To be extended:
        Once the logging facilities are setup other parts of the configuration can be
        processed."""
        # To extend it, see "QAgentConf._post_process_configuration"
        self.logger.info(CONF_READ_MSG.format(config_file=self._config_file))
        self._qmaster_from_config_file()

    def _qmaster_from_config_file(self):
        self.qmaster = {
            QMASTER_HOST_KEY: QMASTER_HOST,
            QAGENT_TO_QMASTER_DATA_PORT_KEY: QAGENT_TO_QMASTER_DATA_PORT,
        }
        try:
            self.qmaster.update(self._config_file_conf[QMASTER_PROGRAM])
        except KeyError:
            pass

    def _logging_from_config_file(self):
        valid_keys = (
            OWN_LOG_FILE_KEY, OWN_LOG_LEVEL_KEY,
            OWN_LOG_MAXBYTES_KEY, OWN_LOG_BACKUPCOUNT_KEY
        )
        self.logging = {
            OWN_LOG_FILE_KEY: DEFAULT_OWN_FILE_LOGGING_PATH,
            OWN_LOG_LEVEL_KEY: DEFAULT_OWN_FILE_LOGGER_LEVEL,
        }
        for key in valid_keys:
            try:
                value = self._config_file_conf[OWN_LOG_SECTION][key]
            except KeyError:
                pass
            else:
                if key == OWN_LOG_MAXBYTES_KEY:
                    value = int(value)
                self.logging[key] = value

    def _create_cl_parser(self):
        parser = argparse.ArgumentParser(description=self.description)
        self._cl_parser = parser

    def _add_arguments(self):
        for name, arg in (ACTION_ARGUMENT, PIDFILE_ARGUMENT, CONFIGFILE_ARGUMENT):
            args, kwargs = arg
            if name in self.default_values:
                kwargs["default"] = self.default_values[name]
            self._cl_parser.add_argument(*args, **kwargs)
        
    def _parse_arguments(self):
        args = self._cl_parser.parse_args(self._argv)
        self._command_line_conf = vars(args)

    def __getitem__(self, key):
        return self._command_line_conf[key]


class QAgentConf(QuloDConf):
    description = QAGENT_DESCRIPTION
    default_values = {
        PIDFILE_STR: QAGENT_DEFAULT_PIDFILE,
        CONFIGFILE_STR: QAGENT_DEFAULT_CONFIGFILE
    }
    
    def _post_process_configuration(self):
        super()._post_process_configuration()
        self._sensors_from_config_file_sections()

    def _sensors_from_config_file_sections(self):
        # In the future, sensors should be a property, maybe dynamically generated
        self.sensors = []
        sections = self._config_file_conf.sections()
        for section in sections:
            sensor = self._make_sensor_from_section(section)
            if sensor:
                self.sensors.append(sensor)

    def _make_sensor_from_section(self, section):
        splitted_section = section.partition(":")
        sensor = None
        if splitted_section[0] == "sensor":
            sensor_name = splitted_section[2]
            options = self._config_file_conf[section]
            try:
                sensor = sensor_factory(sensor_name, options, self.logging)
            except NameError:
                self.logger.error(PROTO_INVALID_SENSOR_MSG.format(sensor_name=sensor_name))
        return sensor

        
class QMasterConf(QuloDConf):
    description = QMASTER_DESCRIPTION
    default_values = {
        PIDFILE_STR: QMASTER_DEFAULT_PIDFILE,
        CONFIGFILE_STR: QMASTER_DEFAULT_CONFIGFILE
    }

    def _post_process_configuration(self):
        super()._post_process_configuration()
        self._graphite_from_config_file()
        
    def _graphite_from_config_file(self):
        self.graphite = {
            GRAPHITE_HOST_KEY: GRAPHITE_HOST,
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: GRAPHITE_CARBON_RECEIVER_PICKLE_PORT,
        }
        try:
            self.graphite.update(self._config_file_conf[GRAPHITE_SECTION])
        except KeyError:
            pass
    
