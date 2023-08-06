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

import unittest
import os
import sys
import time
import socket
import shutil
from functools import reduce
import glob

from tests.common.program import QAgentWrapper
from tests.functional.base_start_stop import BaseStartStop
from tests.functional.environment import LOCALHOST_FT_ENVIRONMENT, DOCKER_FT_ENVIRONMENT

from qulo.constants import (
    QAGENT_DESCRIPTION, CONF_READ_MSG, QAGENT_DEFAULT_CONFIGFILE,
    PROTO_SENSOR_STARTED_MSG, QAGENT_DEFAULT_CONFIGFILE, PROTO_MEASUREMENT_MSG,
    PROTO_INVALID_SENSOR_MSG, QMASTER_PROGRAM, QMASTER_HOST, QMASTER_HOST_KEY,
    QAGENT_TO_QMASTER_DATA_PORT, QAGENT_TO_QMASTER_DATA_PORT_KEY,
    QAGENT_TO_QMASTER_CONNECTING_MSG,
)
from qulo.qagent import QAGENT_STARTING_MESSAGE, QAGENT_STOP_MESSAGE
from qulo.conf import QAGENT_DEFAULT_PIDFILE

import qulo


class BaseQAgent:
    def prepare_sensors(self, conf):
        """It actually prepares some sensor related messages."""
        sensors = {}
        invalid_sensors = {}
        #all_sensors = qulo.sensors._find_all_sensors()
        all_sensors = [
            "CPUPercent", "VirtualMemory", "CPUTimes", "CPUTimesPercent", "CPUCount",
            "CPUStats", "CPUFreq", "SwapMemory", "DiskPartitions", "DiskUsage",
            "DiskIOCounters", "NetIOCounters", "NetConnections", "NetIFAddrs",
            "NetIFStats", "SensorsTemperatures", "SensorsFans", "SensorsBattery",
            "BootTime", "Users"
        ]
        if self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            #  I can do this because the name attribute will be used in DockerFTEnvironment.__enter__
            # to set the hostname of the container
            host = self.program.name
        else:
            host = socket.gethostname()
            
        for section in conf.sections():
            if section.startswith("sensor:"):
                sensor = section[7:]
                if sensor in all_sensors:
                    sensors[sensor] = {
                        "frequency": conf[section]["time_interval"],
                        "sensor_name": sensor,
                        "start_msg": PROTO_SENSOR_STARTED_MSG.format(
                            sensor_name=sensor,
                            host=host,
                            frequency=conf[section]["time_interval"],
                        ),
                    }
                else:
                    if sensor:
                        invalid_sensors[sensor] = {
                            "error_msg": PROTO_INVALID_SENSOR_MSG.format(
                                sensor_name=sensor
                            )
                        }
        self.invalid_sensors = invalid_sensors
        self.sensors = sensors
        
    
class BasicQAgentFunctionalityTest(BaseStartStop, BaseQAgent, unittest.TestCase):
    def setUp(self):
        self.wrapper_class = QAgentWrapper
        self.program_starting_msg = QAGENT_STARTING_MESSAGE
        self.program_stop_msg = QAGENT_STOP_MESSAGE
        self.program_default_pidfile = QAGENT_DEFAULT_PIDFILE
        self.program_description = QAGENT_DESCRIPTION
        self.program_conf_read_msg = CONF_READ_MSG.format(
            config_file=QAGENT_DEFAULT_CONFIGFILE
        )
        self.program_default_configfile = QAGENT_DEFAULT_CONFIGFILE
        super().setUp()

    def _test_measurements_start_and_stop_controled_by_sensors_in_conf(
            self, config_file_name):
        #  Therefore he prepares a a config file with some valid sensor sections
        # and some invalid ones:
        conf = self.prepare_config_from_file(config_file_name)
        self.prepare_sensors(conf)
        #  After that he starts checking that ``{program}`` is not running before
        # launching it:
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            #  I check only in a so-called local environment because inside a new
            # container we don't need to check if the program runs: 
            self.check_program_running(self.program)

        sensor_start_msgs = tuple(v["start_msg"] for k,v in self.sensors.items())
        sensor_invalid_msgs = tuple(
            v["error_msg"] for k,v in self.invalid_sensors.items()
        )
        self.setup_logparser(target_strings=sensor_start_msgs+sensor_invalid_msgs)
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        # and, again, he launches the program:
        self.program.args = ("start",)
        programs = (self.program,)
        with self.ft_env(*programs) as start_command:
            # he gives some time to the logging system to write the data in the logs:
            self.wait_for_environment(2)
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            # he sees that a message saying that the sensor cpu_percent has started meassuring
            # every 1s:
            for sensor_start_msg in sensor_start_msgs:
                for line in new_lines:
                    if sensor_start_msg in line:
                        break
                else:
                    #program.stop()
                    # print("-"*50)
                    # print("log file:", self.ft_env.log_file_name)
                    # with open(self.ft_env.log_file_name, "r") as f:
                    #     for line in f:
                    #         print(">", line)
                    # print("Trying to find:")
                    # print(sensor_start_msg)
                    # print("...in:")
                    # print("new lines:", new_lines)
                    # print("Old lines (summary):", old_lines_summary)
                    # print("conf:")
                    # for section in conf.sections():
                    #     print("[{}]".format(section))
                    #     for k, v in conf.items(section):
                    #         print("... {}: {}".format(k, v))
                    # print("="*50)
                    # with open(self.ft_env.log_file_name, "r") as f:
                    #     for line in f:
                    #         print(">>", line)
                    self.fail("'{}' not found in the logs".format(sensor_start_msg))
            # he also sees error messages about the sensors that do not exist:
            for invalid_sensor in self.invalid_sensors:
                error_msg = self.invalid_sensors[invalid_sensor]["error_msg"]
                for line in new_lines:
                    if error_msg in line:
                        break
                else:
                    #program.stop()
                    self.fail("'{}' not found in the logs".format(error_msg))
            # Now he waits some seconds to check that the measuraments are indeed correctly
            # reported in the logs:
            wait_t = 2.1*max([float(v["frequency"]) for k,v in self.sensors.items()])
            measurement_mark = PROTO_MEASUREMENT_MSG.format("")
            self.setup_logparser(target_strings=(measurement_mark,))
            self.wait_for_environment(wait_t)
            new_lines = self.tmplogparser.get_new_lines()
            self.assertTrue(len(new_lines) > 0)
            for line in new_lines:
                values = [k in line for k in self.sensors]
                self.assertTrue(reduce(lambda x,y: x or y, values))
                #self.assertIn("CPUPercent", line)
                self.assertIn("DEBUG", line)
                self.assertIn(self.program.hostname, line)
                measurement = line[line.find(measurement_mark)+len(measurement_mark):].strip()
                # he finds very nice that the results of the measurements are eval-able:
                eval(measurement)
            # now he stops the program. # implicitly done in __exit__

    def test_measurements_start_and_stop_only_from_valid_sensors_in_conf_file(self):
        #  Tux has created a simple config file for {program} with some sensors.
        #   He wants to check that the measurements correspond to the sensors that can be
        # found in the config file. The program starts and stops, and the sensors seem to
        # do the same.
        self._test_measurements_start_and_stop_controled_by_sensors_in_conf(
            "qagent-test.1.conf"
        )
        #  Now that he tested the program with a couple of sensors he wants to run it to
        # the full.
        # He runs the program now with a config file that contains a lot of sensors:
        self._test_measurements_start_and_stop_controled_by_sensors_in_conf(
            "qagent-test.3.conf"
        )
        # And, it works! This tool seems suitable for his needs.

    def test_measurements_start_and_stop_with_only_1_sensor_for_every_valid_sensor(self):
        #  Tux, systematic as he is, wants to convince himself that the program
        # really works as expected for every single sensor. At least, he wants to
        # check that the measurements start and stop. So first he prepares the
        # config files:
        cwd = os.path.dirname(__file__)
        data_path = os.path.join(cwd, "data")
        single_sensors_path = os.path.join(data_path, "single.sensor")
        single_sensors_full_path = glob.glob(
            os.path.join(single_sensors_path, "qagent-test*.conf")
        )
        single_sensors = [
            os.path.relpath(p, start=data_path) for p in single_sensors_full_path
        ]
        # Then he runs the qagent program with each of them:
        for sensor in single_sensors:
            try:
                self._test_measurements_start_and_stop_controled_by_sensors_in_conf(
                    sensor
                )
            except Exception as e:
                print(sensor,"failed", file=sys.stderr)
                raise
            else:
                print(sensor,"OK", file=sys.stderr)

    def test_behaviour_if_invalid_sensors_in_conf(self):
        #  Tux has created another config file for {program} with some invalid sensors
        # in it; he wants to test that when the program starts, there is an error message
        # and of course, the program keeps running ignoring the invalid entries.
        self._test_measurements_start_and_stop_controled_by_sensors_in_conf(
            "qagent-test.2.conf"
        )

    def _test_qmaster_section_of_config_file(self, conf_file, host, port):
        trying_to_connect_msg = QAGENT_TO_QMASTER_CONNECTING_MSG.format(
            host_key=QMASTER_HOST_KEY, host=host,
            port_key=QAGENT_TO_QMASTER_DATA_PORT_KEY, port=port,
        )
        self.setup_logparser(target_strings=(trying_to_connect_msg,))
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        # and, he launches qagent:
        self.program.args = ("start",)
        programs = (self.program,)
        with self.ft_env(*programs) as start_command:
            self.wait_for_environment(1)
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            # He finds in the logs a message claiming that the connection is established
            # with qmaster
            self.assertEqual(
                old_lines_summary[1][trying_to_connect_msg]+1,
                new_lines_summary[1][trying_to_connect_msg]
            )
            # so he stops qagent with satisfaction.

    def test_keys_in_qmaster_section_are_read_and_reported(self):
        #  Not that the basic checks have passed, Tux plans to run the system
        # in a small partition of the cluster.
        #  But before doing so, he needs to be sure that the host where the
        # qmaster program runs can be given in the configuration file of the
        # qagent program (obviously, the default localhost is not very useful).
        #  So Tux prepares a conf file for qagent with customized "host" and
        # "incoming data port" keys in the "qmaster" section:
        conf_file = "qagent-test.4.conf"
        conf = self.prepare_config_from_file(conf_file)
        host = conf[QMASTER_PROGRAM][QMASTER_HOST_KEY]
        port = conf[QMASTER_PROGRAM][QAGENT_TO_QMASTER_DATA_PORT_KEY]
        self._test_qmaster_section_of_config_file(conf_file, host, port)
        # ...but wait, wait. He wonders what happens if there is no qmaster section
        conf_file = "qagent-test.empty.conf"
        conf = self.prepare_config_from_file(conf_file)
        host = QMASTER_HOST
        port = QAGENT_TO_QMASTER_DATA_PORT
        #self._test_qmaster_section_of_config_file(conf_file, host, port)
        # ...or if the section is empty
        conf_file = "qagent-test.5.conf"
        conf = self.prepare_config_from_file(conf_file)
        self._test_qmaster_section_of_config_file(conf_file, host, port)
        # ...or it has only one key (the host)
        conf_file = "qagent-test.6.conf"
        conf = self.prepare_config_from_file(conf_file)
        host = conf[QMASTER_PROGRAM][QMASTER_HOST_KEY]
        port = QAGENT_TO_QMASTER_DATA_PORT
        self._test_qmaster_section_of_config_file(conf_file, host, port)
        # ...or only the port is given
        conf_file = "qagent-test.7.conf"
        conf = self.prepare_config_from_file(conf_file)
        host = QMASTER_HOST
        port = conf[QMASTER_PROGRAM][QAGENT_TO_QMASTER_DATA_PORT_KEY]
        self._test_qmaster_section_of_config_file(conf_file, host, port)
        # He has to admit that the program seems to be passing all the checks and looks
        # it is ready for production!

        
