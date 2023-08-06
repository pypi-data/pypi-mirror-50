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
from unittest.mock import patch, MagicMock, call, mock_open
from inspect import signature, Parameter

import qulo.qulod
from qulo.constants import (
    PROTO_NO_PERMISSION_PIDFILE, START_STOP_ERROR, PIDFILE_NOT_FOUND,
    PIDFILE_ACTION_CREATED, PIDFILE_ACTION_ACCESSED, INVALID_PID,
    PROCESS_DOES_NOT_EXIST, OWN_LOG_FILE_KEY, ACTION_STR, PIDFILE_STR,
    OWN_LOG_SECTION, 
)


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.main = qulo.qulod.main
        
    def test_is_executable(self):
        self.assertIn("__call__", dir(self.main))

    def test_takes_no_arguments(self):
        s = signature(self.main)
        parameters = s.parameters
        self.assertEqual(len(parameters), 0)

    @patch("qulo.qulod.generic_main")
    @patch("qulo.qulod.QuloD")
    @patch("qulo.qulod.QuloDConf")
    def test_calls_generic_main(self, pqulodconf, pqulod, pgeneric_main):
        self.main()
        pgeneric_main.assert_called_once_with(pqulodconf, pqulod)

        
class QuloDTestCase(unittest.TestCase):
    def setUp(self):
        self.test_class = qulo.qulod.QuloD
        self.mocked_conf = MagicMock()
        setattr(self.mocked_conf, ACTION_STR, "")
        setattr(self.mocked_conf, PIDFILE_STR, "")
        self.simple_logging = {OWN_LOG_FILE_KEY: "/dev/null"}
        setattr(self.mocked_conf, OWN_LOG_SECTION, self.simple_logging)
        with patch("qulo.qulod.setup_logging") as psetup_logging:
            self.psetup_logging = psetup_logging
            self.simple_instance = self.test_class(self.mocked_conf)
        
    def test_instance_has_conf_attribute(self):
        self.assertEqual(self.simple_instance._conf, self.mocked_conf)
        
    def test_instance_has_expected_attributes(self):
        from qulo.qulod import ACTION_STR, PIDFILE_STR
        action_mock = MagicMock()
        pidfile_mock = MagicMock()
        def getitem(key):
            if key == ACTION_STR:
                return action_mock
            elif key == PIDFILE_STR:
                return pidfile_mock
            else:
                raise KeyError
        conf = MagicMock()
        conf.__getitem__.side_effect = getitem
        with patch("qulo.qulod.setup_logging") as psetup_logging:
            instance = self.test_class(conf)
        self.assertEqual(instance.action, conf[ACTION_STR])
        self.assertEqual(instance.pidfile, conf[PIDFILE_STR])
        self.assertEqual(instance.logger, psetup_logging.return_value)

    def test_instance_defines_some_strings(self):
        """This test must be implemented for the subclasses. The rest is not necessary, for
        now."""
        from qulo.qulod import (
            QULOD_STARTING_MESSAGE, QULOD_STOP_MESSAGE, QULOD_CANT_STOP_MESSAGE
        )
        inst = self.simple_instance
        self.assertEqual(inst._starting_message, QULOD_STARTING_MESSAGE)
        self.assertEqual(inst._stopped_message, QULOD_STOP_MESSAGE)
        self.assertEqual(inst._cant_stop_message, QULOD_CANT_STOP_MESSAGE)
        
    def test_instance_setups_logging(self):
        self.psetup_logging.assert_called_once_with(
            logger_name=self.test_class.__name__, rotatingfile_conf=self.mocked_conf.logging)

    @patch("qulo.qulod.setup_logging")
    @patch("qulo.qulod.asyncio.get_event_loop")
    def test_init_creates_event_loop(self, pget_event_loop, psetup_logging):
        event_loop = MagicMock()
        pget_event_loop.return_value = event_loop
        conf = MagicMock()
        instance = self.test_class(conf)
        pget_event_loop.assert_called_once_with()
        self.assertEqual(instance._event_loop, event_loop)

    def test_call_uses_getattr_to_select_action(self):
        action_mock = MagicMock()
        instance = self.simple_instance
        instance.action = action_mock
        pgetattr_ret = MagicMock()
        with patch("qulo.qulod.getattr") as pgetattr:
            pgetattr.return_value = pgetattr_ret
            instance()
        pgetattr.assert_called_once_with(instance, action_mock)
        pgetattr_ret.assert_called_once_with()

    def test_logger_sends_message_to_logger(self):
        instance = self.test_class(self.mocked_conf)
        msg = "my dummy message"
        with self.assertLogs(qulo.qulod.QuloD.__name__) as log:
            instance.logger.info(msg)
        
    @patch("qulo.qulod.QuloD.run")
    @patch("qulo.qulod.daemonize")
    def test_start_call_sequence(self, pdaemonize, prun):
        pidfile_mock = MagicMock()
        logger = MagicMock()
        logger.warning = MagicMock()
        self.simple_instance.pidfile = pidfile_mock
        self.simple_instance.logger = logger
        manager = MagicMock()
        manager.attach_mock(pdaemonize, "daemonize")
        manager.attach_mock(logger.warning, "warning")
        manager.attach_mock(prun, "run")
        self.simple_instance.start()
        msg = self.simple_instance._starting_message
        expected_calls = [
            call.daemonize(pidfile_mock), call.warning(msg), call.run()
        ]
        manager.assert_has_calls(expected_calls)

    @patch("qulo.qulod.QuloD.run")
    @patch("qulo.qulod.daemonize")
    def test_start_behaviour_if_daemonize_raises_RuntimeError(self, pdaemonize, prun):
        from qulo.qulod import START_STOP_ERROR
        import sys
        logger_name = self.simple_instance.__class__.__name__
        from qulo.logs import setup_logging
        logger = setup_logging(logger_name=logger_name, rotatingfile_conf=self.simple_logging)
        self.simple_instance.logger = logger
        pidfile_mock = MagicMock()
        self.simple_instance.pidfile = pidfile_mock
        msg = "my funny error"
        log_level = "ERROR"
        error = RuntimeError(msg)
        pdaemonize.side_effect = error
        expected_log_error = "{}:{}:{}".format(
            log_level, logger_name, msg
        )
        warn_msgs = ("wanna", "be", "porquerizo")
        expected_log_warnings = [
            "{}:{}:{}".format("WARNING", logger_name, msg) for msg in warn_msgs
        ]
        error.to_warning = warn_msgs
        with self.assertRaises(SystemExit) as e:
            with self.assertLogs(qulo.qulod.QuloD.__name__) as log_msg:
                self.simple_instance.start()
        self.assertEqual(e.exception.code, START_STOP_ERROR)
        self.assertIn(expected_log_error, log_msg.output)
        for warn in expected_log_warnings:
            self.assertIn(warn, log_msg.output)
        prun.assert_not_called()

    @patch("qulo.qulod.QuloD.run")
    @patch("qulo.qulod.daemonize")
    def test_start_behaviour_if_daemonize_raises_PermissionError(self, pdaemonize, prun):
        exception_msg = "another funny error"
        error = PermissionError(exception_msg)
        error.to_error = PROTO_NO_PERMISSION_PIDFILE.format(
            pidfile=self.simple_instance.pidfile, action=PIDFILE_ACTION_CREATED)
        pdaemonize.side_effect = error
        logger_name = self.simple_instance.__class__.__name__
        from qulo.logs import setup_logging
        logger = setup_logging(logger_name=logger_name, rotatingfile_conf=self.simple_logging)
        self.simple_instance.logger = logger
        expected_log_critical = "{}:{}:{}: {}".format(
            "WARNING", logger_name, "Exception message", exception_msg
        )
        expected_log_error = "{}:{}:{}".format(
            "ERROR", logger_name, error.to_error
        )
        with self.assertRaises(SystemExit) as e:
            with self.assertLogs(qulo.qulod.QuloD.__name__) as log_msg:
                self.simple_instance.start()
        self.assertEqual(e.exception.code, START_STOP_ERROR)
        prun.assert_not_called()
        self.assertIn(expected_log_critical, log_msg.output)
        self.assertIn(expected_log_error, log_msg.output)

    @patch("qulo.qulod.os.kill")
    def test_stop_kills_right_process_if_pidfile_can_be_opened(self, pkill):
        import signal
        mpid = "9292929292929"
        with patch("qulo.qulod.open", mock_open(read_data=mpid)) as mopen:
            self.simple_instance.stop()
            pkill.assert_called_once_with(int(mpid), signal.SIGTERM)

    @patch("qulo.qulod.os.kill")
    def test_stop_logs_message_if_process_stops(self, pkill):
        with patch("qulo.qulod.open", mock_open(read_data=" 23 \n")) as mopen:
            self.simple_instance.stop()
        self.simple_instance.logger.warning.assert_called_once_with(
            self.simple_instance._stopped_message
        )
        
    # @patch("qulo.qulod.os.path.exists")
    # @patch("qulo.qulod.os.kill")
    # def test_stop_doesnt_kill_if_no_pidfile(self, pkill, pexists):
    #     pexists.return_value = False
    #     self.simple_instance.stop()
    #     pkill.assert_not_called()

    @patch("qulo.qulod.os.kill")
    def test_stop_cleanup_behaviour_if_no_pidfile(self, pkill):
        pidfile_mock = MagicMock()
        self.simple_instance.pidfile = pidfile_mock
        with patch("qulo.qulod.open", mock_open()) as mopen:
            mopen.side_effect = FileNotFoundError
            with self.assertRaises(SystemExit) as system_exit:
                self.simple_instance.stop()
        self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
        pkill.assert_not_called()
        self.simple_instance.logger.error.assert_called_once_with(
            "{}: {}".format(self.simple_instance._cant_stop_message,
                            PIDFILE_NOT_FOUND.format(pidfile=pidfile_mock))
        )

    @patch("qulo.qulod.os.kill")
    def test_stop_cleanup_behaviour_if_no_permission_to_read_pidfile(self, pkill):
        #pidfile_mock = MagicMock()
        #self.simple_instance.pidfile = pidfile_mock
        with patch("qulo.qulod.open", mock_open()) as mopen:
            mopen.side_effect = PermissionError
            with self.assertRaises(SystemExit) as system_exit:
                self.simple_instance.stop()
        self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
        pkill.assert_not_called()
        self.simple_instance.logger.error.assert_called_once_with(
            "{}: {}".format(
                self.simple_instance._cant_stop_message,
                PROTO_NO_PERMISSION_PIDFILE.format(
                    pidfile=self.simple_instance.pidfile, action=PIDFILE_ACTION_ACCESSED))
        )

    @patch("qulo.qulod.os.kill")
    def test_stop_cleanup_behaviour_if_invalid_pids(self, pkill):
        for data, ex in zip(("333998294434332", "asds"), (OverflowError, ValueError)):
            pkill.side_effect = ex
            with patch("qulo.qulod.open", mock_open(read_data=data)) as mopen:
                with self.assertRaises(SystemExit) as system_exit:
                    self.simple_instance.stop()
            self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
            self.simple_instance.logger.error.assert_called_once_with(
                "{}: {}".format(
                    self.simple_instance._cant_stop_message,
                    INVALID_PID.format(pid=data))
            )
            self.simple_instance.logger.error.reset_mock()
        
    @patch("qulo.qulod.os.kill")
    def test_stop_cleanup_behaviour_no_process(self, pkill):
        pidfile_mock = MagicMock()
        self.simple_instance.pidfile = pidfile_mock
        with patch("qulo.qulod.open", mock_open(read_data=" 34324")) as mopen:
            pkill.side_effect = ProcessLookupError
            with self.assertRaises(SystemExit) as system_exit:
                self.simple_instance.stop()
        self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
        self.simple_instance.logger.error.assert_called_once_with(
            "{}: {}".format(
                self.simple_instance._cant_stop_message,
                PROCESS_DOES_NOT_EXIST.format(pid="34324"))
        )
        
    @patch("qulo.qulod.QuloD._clean_up")
    def test_run_loop_call_sequence(self, _clean_up):
        event_loop = MagicMock()
        run_forever = MagicMock()
        event_loop.run_forever = run_forever
        manager = MagicMock()
        manager.attach_mock(run_forever, "run_forever")
        manager.attach_mock(_clean_up, "_clean_up")
        expected_calls = [call.run_forever(), call._clean_up()]
        self.simple_instance._event_loop = event_loop
        self.simple_instance._run_loop()
        manager.assert_has_calls(expected_calls)

    @patch("qulo.qulod.QuloD._clean_up")
    def test_run_loop_calls_loop_close_method_even_if_exception_raises(self, _clean_up):
        event_loop = MagicMock()
        run_forever = MagicMock()
        run_forever.side_effect = Exception()
        event_loop.run_forever = run_forever
        self.simple_instance._event_loop = event_loop
        with self.assertRaises(Exception):
            self.simple_instance._run_loop()
        _clean_up.assert_called_once_with()

    def test_clean_up_calls_event_loop_close(self):
        event_loop = MagicMock()
        self.simple_instance._event_loop = event_loop
        self.simple_instance._clean_up()
        event_loop.close.assert_called_once_with()
    
    @patch("qulo.qulod.QuloD._run_loop")
    def test_run_calls_run_loop(self, prun_loop):
        self.simple_instance.run()
        prun_loop.assert_called_once_with()

    def test_submit_task_arguments(self):
        s = signature(self.simple_instance.submit_task)
        parameters = s.parameters
        param_kinds = [param.kind for param in parameters.values()]
        expected_params = [
            Parameter.POSITIONAL_OR_KEYWORD, Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD
        ]
        self.assertEqual(expected_params, param_kinds)

    def test_submit_task_calls_loop_create_task_method(self):
        event_loop = MagicMock()
        self.simple_instance._event_loop = event_loop
        task = MagicMock()
        returned_task = MagicMock()
        task.return_value = returned_task
        args = MagicMock()
        kwargs = MagicMock()
        self.simple_instance.submit_task(task, *args, **kwargs)
        task.assert_called_once_with(*args, **kwargs)
        event_loop.create_task.assert_called_once_with(returned_task)

        
if __name__ == "__main__":
    unittest.main()
