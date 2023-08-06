#!/bin/env python

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

import unittest
import psutil
import time
import os

from tests.functional.base_start_stop import BaseStartStop
from tests.common.program import QULoDWrapper
from tests.common.logs import LogParser
#from qulo.constants import QULOD_PROCESS_NAME#, QULOD_LOCK_FILE_NAME
from qulo.conf import QULOD_DEFAULT_PIDFILE
from qulo.qulod import QULOD_STARTING_MESSAGE, QULOD_STOP_MESSAGE
from qulo.constants import (
    DEFAULT_OWN_FILE_LOGGING_PATH, QULOD_DESCRIPTION, CONF_READ_MSG, QULOD_DEFAULT_CONFIGFILE,
)


class BasicQulodFunctionalityTest(BaseStartStop, unittest.TestCase):
    def setUp(self):
        self.wrapper_class = QULoDWrapper
        self.program_starting_msg = QULOD_STARTING_MESSAGE
        self.program_stop_msg = QULOD_STOP_MESSAGE
        self.program_default_pidfile = QULOD_DEFAULT_PIDFILE
        self.program_description = QULOD_DESCRIPTION
        self.program_conf_read_msg = CONF_READ_MSG.format(
            config_file=QULOD_DEFAULT_CONFIGFILE
        )
        self.program_default_configfile = QULOD_DEFAULT_CONFIGFILE
        super().setUp()

class SystemScriptStartStopTest(unittest.TestCase):
    def setUp(self):
        cwd = os.path.dirname(__file__)
        conf_file = os.path.join(cwd, "..", "data", "qulo.conf")
        conf_file = os.path.normpath(conf_file)
        self.read_qulo_conf(conf_file)
        from tests.common.init import InitScript
        self.qulo_init_script = InitScript(non_default_conf_file=conf_file)
        self.syslog_parser = LogParser(
            "/var/log/syslog",
            id_strings=(QULOD_PROCESS_NAME,))
        # self.initial_syslog_lines = self.syslog_parser.get_lines(
        #     QULOD_PROCESS_NAME
        # )

    def read_qulo_conf(self, conf_file):
        from configparser import ConfigParser
        cfg = ConfigParser()
        section_header = ["[qulod]\n"]
        with open(conf_file) as conff:
            conf_contents = conff.readlines()
        conf_str = ''.join(section_header + conf_contents)
        cfg.read_string(conf_str)
        self.qulo_config = cfg
        
    def find_qulod(self):
        qulod_process = None
        for process in psutil.process_iter():
            if process.name() == QULOD_PROCESS_NAME:
                qulod_process = process
                break
        return qulod_process

    def find_qulod_PID_from_lock_file(self):
        #lock_file_name = QULOD_LOCK_FILE_NAME
        from qulo.global_conf import QULOD_PIDFILE_VAR
        lock_file_name = self.qulo_config.get("qulod", QULOD_PIDFILE_VAR)
        if os.path.exists(lock_file_name):
            with open(lock_file_name) as lock_file:
                pid_full = lock_file.read().strip()
            pid = int(pid_full)
        else:
            pid = None
        return pid
        

@unittest.skip
class BasicQulodFunctionalityInitScriptTest(SystemScriptStartStopTest):
    def test_qulod_starts_and_stops(self):
        #  Tux is one of our system administrators. He is testing the new
        # cluster perfromance tool written by one of the local hpc-support 
        # fellows.
        #  Tux likes the Unix philosophy. Well, "likes" is not very precise. 
        # He *loves* Unix. Of course, he assumes that this new tool 
        # fulfils his expectations for services. To start with, he checks 
        # that ``qulod`` is not running before launching it:
        qulod_process = self.find_qulod()
        if qulod_process:
            self.fail(
                "'qulod' process found before starting! Stop it and come back to test."
            )
        #  Fine, now he can start testing this new promising tool!
        # For that, he launches the "qulod" init script:
        self.qulo_init_script.start()
        # and as a consequence, he expects to find a running process 
        # named properly:
        time.sleep(0.5)#need a bit of sleep to catch the process
        qulod_process = self.find_qulod()
        if not qulod_process:
            self.fail("No 'qulod' process found!")
        # He also expects the creation of a lock file with the PID in it:
        found_pid = self.find_qulod_PID_from_lock_file()
        # which agrees with the PID of the process:
        self.assertEqual(found_pid, qulod_process.pid)
        #  At this point, he wants to check what happens with the logs. 
        # And he checks with satisfaction that the start event is 
        # registered in the system log. First a line informing that the 
        # daemon is starting is found. Second, he also finds a line 
        # claiming that the daemon started (he understands, it means that
        # the process of starting the daemon concluded):
        new_log_entries = self.syslog_parser.get_new_lines()
        string_marks_msg = "'{0}' and '{1}' not found in the same log file line"
        string_marks_list = [
            (QULOD_PROCESS_NAME, "starting"),
            (QULOD_PROCESS_NAME, "started"),
        ]
        for string_marks in string_marks_list:
            for log_line in new_log_entries:
                if string_marks[0] in log_line and string_marks[1] in log_line:
                    break
            else:
                self.fail(string_marks_msg.format(*string_marks))
        #  Of course, at the same time he checks that there is no message 
        # in the log file informing that the daemon stopped
        string_marks_msg = "'{0}' and '{1}' found in the same log file line!"
        string_marks_list = [
            (QULOD_PROCESS_NAME, "stopped"),
        ]
        for string_marks in string_marks_list:
            for log_line in new_log_entries:
                if string_marks[0] in log_line and string_marks[1] in log_line:
                    self.fail(string_marks_msg.format(*string_marks))
        # To conclude this first tour, only one thing is missing, namely that
        # issuing the "stop" command:
        self.qulo_init_script.stop(wait=6)
        # effectively kills "qulod"
        qulod_process = self.find_qulod()
        self.assertIs(qulod_process, None)
        # ...and the software registers that event in the system log:
        new_log_entries = self.syslog_parser.get_new()
        string_marks_msg = "'{0}' and '{1}' not found in the same log file line"
        string_marks_list = [
            (QULOD_PROCESS_NAME, "stopping"),
            (QULOD_PROCESS_NAME, "stopped"),
        ]
        for string_marks in string_marks_list:
            for log_line in new_log_entries:
                if string_marks[0] in log_line and string_marks[1] in log_line:
                    break
            else:
                self.fail(string_marks_msg.format(*string_marks))
        # that concludes the first test he makes to the functionality of the 
        # new monitoring program.
        
    def test_right_qulo_config_is_read_when_init_script_starts(self):
        #  When the qulo script starts, it is reported what options are found 
        # in the configuration file 
        self.fail("implement it! (WIP): qulo.conf")
        # check for QULOD_CONF, QULOD_PIDFILE, ...
        
    def test_qulo_does_not_start_if_host_mismatch(self):
        fail_message = "Move it to the qulod test: The 'host' read in "\
          "the conf file must agree with hostname"
        self.fail(fail_message)
