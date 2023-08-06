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
import time
import socket
import shutil
from functools import reduce

from tests.common.program import QMasterWrapper, QAgentWrapper
from tests.functional.base_start_stop import BaseStartStop
from tests.functional.test_qagent import BaseQAgent
from tests.functional.environment import (
    LOCALHOST_FT_ENVIRONMENT, DOCKER_FT_ENVIRONMENT, 
)
from qulo.constants import (
    QMASTER_DESCRIPTION, CONF_READ_MSG, QMASTER_DEFAULT_CONFIGFILE,
    QAGENT_DEFAULT_CONFIGFILE, PROTO_SENSOR_STARTED_MSG, QMASTER_DEFAULT_CONFIGFILE,
    PROTO_MEASUREMENT_RECEIVED_MSG, PROTO_INVALID_SENSOR_MSG,
)
from qulo.qmaster import QMASTER_STARTING_MESSAGE, QMASTER_STOP_MESSAGE
from qulo.conf import QMASTER_DEFAULT_PIDFILE, QAGENT_DEFAULT_PIDFILE

import qulo


class QMasterFunctionalityDefaultConfTest(BaseStartStop, BaseQAgent, unittest.TestCase):
    def setUp(self):
        self.wrapper_class = QMasterWrapper
        self.program_starting_msg = QMASTER_STARTING_MESSAGE
        self.program_stop_msg = QMASTER_STOP_MESSAGE
        self.program_default_pidfile = QMASTER_DEFAULT_PIDFILE
        self.program_description = QMASTER_DESCRIPTION
        self.program_conf_read_msg = CONF_READ_MSG.format(
            config_file=QMASTER_DEFAULT_CONFIGFILE
        )
        self.program_default_configfile = QMASTER_DEFAULT_CONFIGFILE
        super().setUp()

    def test_qmaster_communicates_with_qagent(self):
        #  Tux has wants to check that qmaster and qagent can communicate.
        # So, he prepares configurations files for qmaster and qagent:
        qagent = QAgentWrapper(pidfile=QAGENT_DEFAULT_PIDFILE)
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            qagent_config_file_name = "qagent-test.1.conf"
            qmaster_config_file_name = "qmaster.1.conf"
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            qagent_config_file_name = "qagent-test.1.docker.conf"
            qmaster_config_file_name = "qmaster.1.docker.conf"
        qagent_conf = self.prepare_config_from_file(
            qagent_config_file_name, default_configfile=QAGENT_DEFAULT_CONFIGFILE, program=qagent,
        )
        self.prepare_sensors(qagent_conf)
        qmaster_conf = self.prepare_config_from_file(qmaster_config_file_name)
        #and he launches qmaster and qagent:
        self.program.args = ("start",)
        qagent.args = ("start",)
        programs = (self.program, qagent)
        ## I need to remove some spaces and one ":" to be able to identify lines
        measurament_received = PROTO_MEASUREMENT_RECEIVED_MSG.format("", "")
        measurament_received = measurament_received.strip().strip(":").strip()
        self.setup_logparser(target_strings=(measurament_received,))
        old_lines = self.tmplogparser.get_new_lines()
        with self.ft_env(*programs) as start_qmaster_qagent:
            # Now he waits some seconds to check that the measuraments are indeed correctly
            # reported in the logs, *as received messages*:
            wait_t = 2.1*max([float(v["frequency"]) for k,v in self.sensors.items()])
            self.wait_for_environment(wait_t)
            new_lines = self.tmplogparser.get_new_lines()
            print(
                "file:", self.ft_env.log_file_name,
                "old lines:", old_lines,
                "new lines:", new_lines,
                sep="\n  "
            )
            self.assertTrue(len(new_lines) > 0)
            for line in new_lines:
                values = [k in line for k in self.sensors]
                self.assertTrue(reduce(lambda x,y: x or y, values))
                self.assertIn("DEBUG", line)
                self.assertIn("QMaster", line)
        # This was very satisfying!
        # He stops qagent:
    # and qmaster:

