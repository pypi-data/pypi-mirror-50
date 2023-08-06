#!/bin/env python3

#######################################################################
# Copyright (C) 2016, 2018, 2019 David Palao
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

import logging

PROTO_STARTING_PROGRAM_MSG = "Starting {program}..."
PROTO_STOPPED_PROGRAM_MSG = "{program} stopped"
PROTO_CANT_STOP_MSG = "{program} could not be stopped"
NOT_RUNNING_MESSAGE = "Not running"
START_STOP_ERROR = 1
ALREADY_RUNNING_MSG = 'It looks it is already running'

CONFIGFILE_STR = "config_file"

DEFAULT_PID_DIR = "/run"
DEFAULT_PROTO_PIDFILE = "{program}.pid"
QULOD_PROGRAM = "qulod"
QULOD_DESCRIPTION = "qulo program"
QULOD_DEFAULT_CONFIGFILE = "/etc/qulo/qulod.conf"
QAGENT_DEFAULT_CONFIGFILE = "/etc/qulo/qagent.conf"
QMASTER_DEFAULT_CONFIGFILE = "/etc/qulo/qmaster.conf"

QAGENT_PROGRAM = "qagent"
QAGENT_DESCRIPTION = """qulo agent is a daemon program that measures performance data in the host computer
and transfers that data to the qulo master program"""

QMASTER_PROGRAM = "qmaster"
QMASTER_DESCRIPTION = "qulo master program"
SERVING_PROTO_MESSAGE = "Serving on {}"
INITIAL_QMASTER_SERVER_PACKET_SIZE = 8192

ACTION_STR = "action"
ACTION_HELP = "action to perform."
ACTION_START = "start"
ACTION_STOP = "stop"
ACTION_CHOICES = [ACTION_START, ACTION_STOP]

PIDFILE_OPTION_ALIASES = ("-p", "--pidfile")
PIDFILE_STR = "pidfile"
PIDFILE_HELP = "provide an alternative PID file name (default: %(default)s)"
PIDFILE_ACTION_CREATED = "created"
PIDFILE_ACTION_ACCESSED = "accessed"
PROTO_NO_PERMISSION_PIDFILE = "Pidfile ('{pidfile}') cannot be {action}"
PIDFILE_EXISTS = "Pidfile ('{pidfile}') already exists"
PROCESS_DOES_NOT_EXIST = "The process with PID={pid} does not seem to exist"
RUNNING_PROCESS_FOUND = "There is a running process with PID={pid}"
NO_PID_FOUND = "No PID found"
PIDFILE_NOT_FOUND = "Pidfile ('{pidfile}') does not exist"
INVALID_PID = "PID='{pid}' is invalid"

CONFIGFILE_STR = "file"
CONFIGFILE_OPTION_ALIASES = ("-c", "--config")
CONFIGFILE_HELP = "provide an alternative config file name (default: %(default)s)"
DEFAULT_CONFIG_FILE = QULOD_DEFAULT_CONFIGFILE
CONF_READ_MSG = "Global conf read from file {config_file}"

GENERIC_CONNECTED_MSG = " ...connection established"

# Logging:
LOGGER_LEVEL = logging.DEBUG
OWN_LOG_SECTION = "logging"
OWN_LOG_FILE_KEY = "filename"
OWN_LOG_MAXBYTES_KEY = "maxBytes"
OWN_LOG_BACKUPCOUNT_KEY = "backupCount"
OWN_LOG_LEVEL_KEY = "level"
DEFAULT_OWN_FILE_LOGGER_LEVEL = logging.DEBUG
DEFAULT_OWN_FILE_LOGGING_PATH = "/var/log/qulo.log"
DEFAULT_OWN_FILE_BACKUP_COUNT = 5
DEAFULT_OWN_FILE_MAXBYTES = 134217728
SYSLOG_LOGGER_LEVEL = logging.WARNING
FILE_LOGGING_FORMAT = "%(levelname)s [%(asctime)s][%(name)s] ---> %(message)s"
CANNOT_USE_LOG_HANDLER = "I cannot log! Try to change the log file in the configuration file."

PROTO_SENSOR_STARTED_MSG = "{sensor_name} sensor starts on {host} (freq: 1/{frequency}s)"
PROTO_MEASUREMENT_MSG = "measurement: {}"
PROTO_MEASUREMENT_RECEIVED_MSG = "received from {}: {}"
PROTO_INVALID_SENSOR_MSG = "{sensor_name}: invalid sensor name; ignored"
PROTO_MSG_TO_GRAPHITE = "[to graphite] {}"

DEFAULT_HOST_KEY = "host"
QMASTER_HOST_KEY = DEFAULT_HOST_KEY
QMASTER_HOST = "127.0.0.1"

QAGENT_TO_QMASTER_DATA_PORT_KEY = "incoming data port"
QAGENT_TO_QMASTER_DATA_PORT = 7888

QAGENT_TO_QMASTER_CONNECTING_MSG = (
    "Connecting to qmaster ({host_key}={host}, {port_key}={port}) to send data from sensors..."
)
QAGENT_TO_QMASTER_CONNECTED_MSG = GENERIC_CONNECTED_MSG

GRAPHITE_SECTION = "Graphite"
GRAPHITE_HOST_KEY = DEFAULT_HOST_KEY
GRAPHITE_HOST = "localhost"
GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY = "carbon receiver pickle port"
GRAPHITE_CARBON_RECEIVER_PICKLE_PORT = 2004
QMASTER_TO_GRAPHITE_CONNECTED_MSG = GENERIC_CONNECTED_MSG
QMASTER_TO_GRAPHITE_CONNECTING_MSG = (
    "Connecting to Graphite ({host_key}={host}, {port_key}={port}) to send data from sensors..."
)
QMASTER_TO_GRAPHITE_RETRY_MSG = "... connection to {host} failed. Retrying."

