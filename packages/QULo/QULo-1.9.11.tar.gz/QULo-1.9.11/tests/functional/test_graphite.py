#!/bin/env python3

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
import time
import os
import socket

from tests.functional.base_start_stop import MultiProgramBaseStartStop
from tests.common.program import QMasterWrapper, QAgentWrapper
from tests.functional.graphite import get_data_from_graphite_render_api
from tests.functional.environment import LOCALHOST_FT_ENVIRONMENT, DOCKER_FT_ENVIRONMENT

from qulo.constants import (
    QMASTER_DEFAULT_CONFIGFILE, QAGENT_DEFAULT_CONFIGFILE,
    QMASTER_TO_GRAPHITE_CONNECTING_MSG, QMASTER_TO_GRAPHITE_CONNECTED_MSG,
    GRAPHITE_HOST_KEY, GRAPHITE_SECTION,
    GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY
)
from qulo.conf import QMASTER_DEFAULT_PIDFILE, QAGENT_DEFAULT_PIDFILE


class BasicGraphiteTestCase(MultiProgramBaseStartStop, unittest.TestCase):
    """First FT for Graphite. It assumes that Graphite is running and checks that
    Graphite gets messages from QULo."""

    default_config_files = (QMASTER_DEFAULT_CONFIGFILE, QAGENT_DEFAULT_CONFIGFILE)
    _WITH_GRAPHITE = True
    
    def test_error_behaviour_of_pidfile_functionality(self):
        #  I want to skip this test from the Base because in that test, the
        # functionality of the program is tested, BUT the BasicGraphiteTestCase
        # is about testing integration between graphite and QULo
        pass

    def test_logging_section_of_config_file(self):
        #  Same as before
        pass

    def test_config_file_can_be_changed_from_command_line(self):
        # and again
        pass
            
    def test_messages_sent_by_qmaster_arrive_to_graphite(self):
        #  Tux has been told by the developers that QULo can communicate with
        # Graphite: it sends metrics to it. He wants to check this feature, that
        # he finds promising.
        # So he prepares config files for qagent and qmaster:
        qmaster = QMasterWrapper(pidfile=QMASTER_DEFAULT_PIDFILE)
        qagent = QAgentWrapper(pidfile=QAGENT_DEFAULT_PIDFILE)
        programs = (qmaster, qagent)
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            simple_conf_files = ("qmaster-graphite.1.conf", "qagent-test.1.conf")
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            simple_conf_files = ("qmaster-graphite.docker.1.conf", "qagent-test.docker.1.conf")
        confs = [
            self.prepare_config_from_file(
                conf4test, default_configfile=def_conf, program=prog,
            ) for conf4test, def_conf, prog in zip(
                simple_conf_files, self.default_config_files, programs)
        ]
        # he restarts graphite, to be sure that there is no cache contaminating the test
        # and when he launches the programs (qmaster and qagent)
        qmaster.args = ("start",)
        qagent.args = ("start",)
        trying_graphite_conn = QMASTER_TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY,
            host=confs[0][GRAPHITE_SECTION][GRAPHITE_HOST_KEY],
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=confs[0][GRAPHITE_SECTION][GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY],
        )
        graphite_connected = QMASTER_TO_GRAPHITE_CONNECTED_MSG
        graphite_lines = (trying_graphite_conn, graphite_connected)
        self.setup_logparser(target_strings=graphite_lines)

        with self.ft_env(*programs) as graphite_qmaster_qagent:
            # he can see that after waiting some little time the connection with graphite
            # is announced in the logs
            self.wait_for_environment(15)
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            for target in graphite_lines:
                for line in new_lines:
                    if target in line:
                        break
                else:
                    self.fail("'{}' not found in the logs".format(target))
            # and actually the two sensors have reported several measurements:
            #time.sleep(1.1)
            ncpus = os.cpu_count()
            hostname = qagent.hostname
            targets = []
            for icpu in range(ncpus):
                targets.append(f"{hostname}.CPUPercent.{icpu}")
            targets.append(f"{hostname}.VirtualMemory.percent")
            for target in targets:
                graphite_data = get_data_from_graphite_render_api(target).strip()
                result = graphite_data.split("|")[1]
                self.assertNotEqual(result, "None")
                self.assertNotEqual(result, "")


if __name__ == "__main__":
    unittest.main()
