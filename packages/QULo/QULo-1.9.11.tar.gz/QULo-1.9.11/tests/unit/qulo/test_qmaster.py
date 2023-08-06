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

from unittest.mock import patch, MagicMock, call, mock_open, PropertyMock
from inspect import signature, Parameter

from tests.unit.qulo.aio_tools import asyncio_run, AsyncioMock

import qulo.qmaster
from qulo.constants import (
    QAGENT_TO_QMASTER_DATA_PORT_KEY, QMASTER_HOST_KEY,
    GRAPHITE_HOST_KEY, GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
    PROTO_MSG_TO_GRAPHITE, QMASTER_TO_GRAPHITE_CONNECTING_MSG,
    QMASTER_TO_GRAPHITE_CONNECTED_MSG, QMASTER_TO_GRAPHITE_RETRY_MSG,
    ACTION_STR, PIDFILE_STR, OWN_LOG_SECTION, OWN_LOG_FILE_KEY, 
)


class InventedException(Exception):
    pass


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.main = qulo.qmaster.main
        
    def test_is_executable(self):
        self.assertIn("__call__", dir(self.main))

    def test_takes_no_arguments(self):
        s = signature(self.main)
        parameters = s.parameters
        self.assertEqual(len(parameters), 0)

    @patch("qulo.qmaster.generic_main")
    @patch("qulo.qmaster.QMaster")
    @patch("qulo.qmaster.QMasterConf")
    def test_calls_generic_main(self, pmasterconf, pmaster, pgeneric_main):
        self.main()
        pgeneric_main.assert_called_once_with(pmasterconf, pmaster)

        
class QMasterTestCase(unittest.TestCase):
    def setUp(self):
        self.test_class = qulo.qmaster.QMaster
        self.mocked_conf = MagicMock()
        setattr(self.mocked_conf, ACTION_STR, "")
        setattr(self.mocked_conf, PIDFILE_STR, "")
        self.simple_logging = {OWN_LOG_FILE_KEY: "/dev/null"}
        setattr(self.mocked_conf, OWN_LOG_SECTION, self.simple_logging)
        self.simple_instance = self.test_class(self.mocked_conf)

    def test_QMaster_is_subclass_of_QuloD(self):
        from qulo.qulod import QuloD
        self.assertTrue(issubclass(self.test_class, QuloD))

    @patch("qulo.qmaster.asyncio.Queue")
    def test_init_creates_to_graphite_queue(self, pQueue):
        to_graphite_queue = MagicMock()
        pQueue.side_effect = [to_graphite_queue]
        instance = self.test_class(self.mocked_conf)
        self.assertEqual(instance._to_graphite_queue, to_graphite_queue)

    @patch("qulo.qmaster.QuloD.__init__")
    def test_init_calls_super_init(self, pinit):
        conf = MagicMock()
        instance = self.test_class(conf)
        pinit.assert_called_once_with(conf)
        
    def test_instance_defines_some_strings(self):
        from qulo.qmaster import (
            QMASTER_STARTING_MESSAGE, QMASTER_STOP_MESSAGE, QMASTER_CANT_STOP_MESSAGE
        )
        inst = self.simple_instance
        self.assertEqual(inst._starting_message, QMASTER_STARTING_MESSAGE)
        self.assertEqual(inst._stopped_message, QMASTER_STOP_MESSAGE)
        self.assertEqual(inst._cant_stop_message, QMASTER_CANT_STOP_MESSAGE)
        
    @patch("qulo.qmaster.QuloD.run")
    @patch("qulo.qmaster.QMaster.submit_task")
    @patch("qulo.qmaster.QMaster._run_server")
    @patch("qulo.qmaster.QMaster._create_server")
    def test_run_call_sequence(self, _create_server, _run_server, submit_task, run):
        manager = MagicMock()
        server = MagicMock()
        _create_server.return_value = server
        manager.attach_mock(_create_server, "_create_server")
        manager.attach_mock(_run_server, "_run_server")
        manager.attach_mock(submit_task, "submit_task")
        manager.attach_mock(run, "run")
        expected_calls = [
            call._create_server(),
            call._run_server(server),
            call.submit_task(self.simple_instance._send_to_graphite),
            call.run(),
        ]
        self.simple_instance.run()
        manager.assert_has_calls(expected_calls)
        
    @patch("qulo.qmaster.asyncio.start_server")
    def test_create_server_calls_to_and_returns_from_start_server(self, start_server):
        server = MagicMock()
        mock_conf = MagicMock()
        self.simple_instance._conf = mock_conf
        host = "ayeleole"
        port = 8686844
        def getitem(value):
            return {QMASTER_HOST_KEY: host, QAGENT_TO_QMASTER_DATA_PORT_KEY: port}[value]
        mock_conf.qmaster.__getitem__.side_effect = getitem
        start_server.return_value = server
        result = self.simple_instance._create_server()
        start_server.assert_called_once_with(
            self.simple_instance._handle_connection, host, port,
            loop=self.simple_instance._event_loop
        )
        self.assertEqual(result, server)

    def test_run_server_sends_coroutine_to_event_loop(self):
        server_coroutine = MagicMock()
        server = MagicMock()
        self.simple_instance._event_loop = MagicMock()
        self.simple_instance._event_loop.run_until_complete.return_value = server
        run_until_complete = self.simple_instance._event_loop.run_until_complete
        self.simple_instance._run_server(server_coroutine)
        run_until_complete.assert_called_once_with(server_coroutine)
        self.assertEqual(server, self.simple_instance.server)

    def test_run_server_sends_message_to_logger(self):
        from qulo.constants import SERVING_PROTO_MESSAGE
        logger = MagicMock()
        server = MagicMock()
        self.simple_instance._event_loop = MagicMock()
        run_until_complete = MagicMock()
        run_until_complete.return_value = server
        self.simple_instance._event_loop.run_until_complete = run_until_complete
        self.simple_instance.logger = logger
        self.simple_instance._run_server(MagicMock())
        message = SERVING_PROTO_MESSAGE.format(server.sockets[0].getsockname())
        logger.info.assert_called_once_with(message)

    @patch("qulo.qmaster.QuloD._clean_up")
    def test_clean_up_call_sequence(self, qulod_clean_up):
        manager = MagicMock()
        close = MagicMock()
        run_until_complete = MagicMock()
        server = MagicMock()
        wait_closed = MagicMock()
        server.wait_closed.return_value = wait_closed
        self.simple_instance.server = server
        event_loop = MagicMock()
        self.simple_instance._event_loop = event_loop
        manager.attach_mock(server, "server")
        manager.attach_mock(event_loop, "_event_loop")
        manager.attach_mock(qulod_clean_up, "_clean_up")
        expected_calls = [
            call.server.close(),
            call.server.wait_closed(),
            call._event_loop.run_until_complete(wait_closed),
            call._clean_up()
        ]
        self.simple_instance._clean_up()
        manager.assert_has_calls(expected_calls)

    def test_handle_connection_is_a_coroutine(self):
        from inspect import iscoroutinefunction
        self.assertTrue(iscoroutinefunction(self.test_class._handle_connection))

    def test_handle_connection_takes_two_parameters(self):
        s = signature(self.simple_instance._handle_connection)
        parameters = s.parameters
        self.assertEqual(len(parameters), 2)

    @patch("qulo.qmaster.pickle.loads")
    def test_handle_connection_awaits_reader_read(self, loads):    
        from qulo.constants import INITIAL_QMASTER_SERVER_PACKET_SIZE
        reader = MagicMock()
        writer = MagicMock()
        for num in 4,1,2:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            reader.read = AsyncioMock(side_effect=values)
            expected_calls_get = [
                call(INITIAL_QMASTER_SERVER_PACKET_SIZE) for value in values[:-1]
            ]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            reader.read.mock.assert_has_calls(expected_calls_get)

    @patch("qulo.qmaster.pickle.loads")
    def test_handle_connection_awaits_to_graphite_queue_put(self, loads):    
        from qulo.constants import INITIAL_QMASTER_SERVER_PACKET_SIZE
        reader = MagicMock()
        writer = MagicMock()
        self.simple_instance._to_graphite_queue = MagicMock()
        for num in 3,2,5:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            reader.read = AsyncioMock(side_effect=values)
            self.simple_instance._to_graphite_queue.put = AsyncioMock()
            expected_calls_put = [call(value) for value in values[:-1]]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            self.simple_instance._to_graphite_queue.put.mock.assert_has_calls(
                expected_calls_put
            )
            self.simple_instance._to_graphite_queue.put.mock.reset_mock()

    @patch("qulo.qmaster.pickle.loads")
    def test_handle_connection_calls_once_to_writer_get_extra_info(self, loads):    
        reader = MagicMock()
        writer = MagicMock()
        extra_info = MagicMock()
        writer.get_extra_info = extra_info
        for num in 6,2,4:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            reader.read = AsyncioMock(side_effect=values)
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            extra_info.assert_called_once_with("peername")
            extra_info.reset_mock()

    @patch("qulo.qmaster.pickle.loads")
    def test_handle_connection_sends_wished_message_to_logger(self, loads):
        from qulo.constants import PROTO_MEASUREMENT_RECEIVED_MSG
        import pickle
        reader = MagicMock()
        writer = MagicMock()
        addr = MagicMock()
        writer.get_extra_info.return_value = addr
        for num in 3,5,1:
            logger = MagicMock()
            self.simple_instance.logger = logger
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            loads_values = [MagicMock() for _ in range(num)]
            loads.side_effect = loads_values
            reader.read = AsyncioMock(side_effect=values)
            log_msgs = [
                PROTO_MEASUREMENT_RECEIVED_MSG.format(addr, msg) for msg in loads_values
            ]
            expected_calls_logger_debug = [call(msg) for msg in log_msgs]
            expected_calls_loads = [call(value) for value in values[:-1]]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            logger.debug.assert_has_calls(expected_calls_logger_debug)
            loads.assert_has_calls(expected_calls_loads)
            loads.reset_mock()
    
    def test_send_to_graphite_is_a_coroutine(self):
        from inspect import iscoroutinefunction
        self.assertTrue(iscoroutinefunction(self.test_class._send_to_graphite))

    @patch("qulo.qmaster.QMessage")
    def test_send_to_graphite_awaits_in_queue_get(self, mock_QMessage):
        with patch(
                "qulo.qmaster.asyncio.open_connection", new=AsyncioMock()
                ) as open_connection:
            reader = MagicMock()
            writer = MagicMock()
            open_connection.mock.return_value = (reader, writer)
            self.simple_instance._to_graphite_queue = MagicMock()
            self.simple_instance._event_loop = MagicMock()
            for num in 4,2,3:
                values = [MagicMock() for _ in range(num)] + [InventedException()]
                self.simple_instance._to_graphite_queue.get = AsyncioMock(
                    side_effect=values)
                self.simple_instance._to_graphite_queue.get.mock.side_effect = values
                expected_calls_get = [call() for value in values[:-1]]
                with self.assertRaises(InventedException):
                    asyncio_run(self.simple_instance._send_to_graphite())
                self.simple_instance._to_graphite_queue.get.mock.assert_has_calls(
                    expected_calls_get)
                self.simple_instance._to_graphite_queue.get.mock.reset_mock()

    @patch("qulo.qmaster.QMessage")
    @patch("qulo.qmaster.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_awaits_open_connection_only_once_if_connection(self, mock_QMessage):
        from qulo.qmaster import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        graphite_conf = {
            GRAPHITE_HOST_KEY: "qaqa",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 212434,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.return_value = (reader, writer)
        for num in 1, 5, 2:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            self.simple_instance._to_graphite_queue.get = AsyncioMock(
                side_effect=values)
            self.simple_instance._to_graphite_queue.get.mock.side_effect = values
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._send_to_graphite())
            mock_open_connection.mock.assert_called_once_with(
                "qaqa", 212434, loop=self.simple_instance._event_loop
            )
            mock_open_connection.mock.reset_mock()

    @patch("qulo.qmaster.QMessage")
    @patch("qulo.qmaster.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_sends_raw_message_to_logger(self, mock_QMessage):
        from qulo.qmaster import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        logger = self.simple_instance.logger
        log_level = "DEBUG"
        log_template = "{}:{}:{}".format(
            log_level, self.simple_instance.__class__.__name__, PROTO_MSG_TO_GRAPHITE,
        )
        mock_open_connection.mock.return_value = (reader, writer)
        for num in 4, 2:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            self.simple_instance._to_graphite_queue.get = AsyncioMock(
                side_effect=values)
            #args = aquin+[QMessage.from_remote(_) for _ in values[:-1]]
            args = values[:-1]
            expected = [log_template.format(_) for _ in args]
            self.simple_instance._to_graphite_queue.get.mock.side_effect = values
            with self.assertRaises(InventedException):
                with self.assertLogs(logger, level=log_level) as log:
                    asyncio_run(self.simple_instance._send_to_graphite())
            for expected_line in expected:
                self.assertIn(expected_line, log.output)

    @patch("qulo.qmaster.QMessage")
    @patch("qulo.qmaster.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_writes_message_to_writer(self, mock_QMessage):
        from qulo.qmaster import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.return_value = (reader, writer)
        
        for num in 1, 3:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            self.simple_instance._to_graphite_queue.get = AsyncioMock(
                side_effect=values)
            #args = aquin+[QMessage.from_remote(_) for _ in values[:-1]]
            args = values[:-1]
            expected_calls = [call(mock_QMessage(_).to_graphite()) for _ in args]
            self.simple_instance._to_graphite_queue.get.mock.side_effect = values
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._send_to_graphite())
            writer.write.assert_has_calls(expected_calls)
            writer.write.reset_mock()

    @patch("qulo.qmaster.asyncio.sleep", new=AsyncioMock())
    @patch("qulo.qmaster.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_awaits_sleep_if_ConnectionRefusedError(self):
        from qulo.qmaster import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        values = [ConnectionRefusedError(), ConnectionRefusedError(), (reader, writer)]
        mock_open_connection.mock.side_effect = values
        self.simple_instance._to_graphite_queue.get = AsyncioMock(side_effect=InventedException())
        expected_calls = [call(1), call(1)]
        with self.assertRaises(InventedException):
            asyncio_run(self.simple_instance._send_to_graphite())
        asyncio.sleep.mock.assert_has_calls(expected_calls)

    @patch("qulo.qmaster.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_logs_if_no_connection(self):
        from qulo.qmaster import asyncio
        mock_open_connection = asyncio.open_connection
        graphite_conf = {
            GRAPHITE_HOST_KEY: "jamacuquen",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 21555,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem        
        logger = self.simple_instance.logger
        log_level = "INFO"
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.side_effect = InventedException()
        expected = QMASTER_TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY,
            host="jamacuquen",
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=21555,
        )
        expected = "{}:{}:{}".format(
            log_level, self.simple_instance.__class__.__name__, expected
        )
        self.simple_instance._to_graphite_queue.get = AsyncioMock(
            side_effect=InventedException())
        with self.assertRaises(InventedException):
            with self.assertLogs(logger, level=log_level) as log:            
                asyncio_run(self.simple_instance._send_to_graphite())
        self.assertIn(expected, log.output)
    
    @patch("qulo.qmaster.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_logs_if_connected_and_no_refused_trials(self):
        from qulo.qmaster import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        graphite_conf = {
            GRAPHITE_HOST_KEY: "jamacuquen",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 21555,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem        
        logger = self.simple_instance.logger
        log_level = "INFO"
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.return_value = (reader, writer)
        expected0 = QMASTER_TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY,
            host="jamacuquen",
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=21555,
        )
        proto = [expected0, QMASTER_TO_GRAPHITE_CONNECTED_MSG]
        cn = self.simple_instance.__class__.__name__
        expected = ["{}:{}:{}".format(log_level, cn, _) for _ in proto]
        self.simple_instance._to_graphite_queue.get = AsyncioMock(
            side_effect=InventedException())
        with self.assertRaises(InventedException):
            with self.assertLogs(logger, level=log_level) as log:            
                asyncio_run(self.simple_instance._send_to_graphite())
        for line in expected:
            self.assertIn(line, log.output)

    @patch("qulo.qmaster.asyncio.sleep", new=AsyncioMock())
    @patch("qulo.qmaster.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_logs_if_connected_but_refused_trials(self):
        from qulo.qmaster import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        graphite_conf = {
            GRAPHITE_HOST_KEY: "gul",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 21555,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem        
        logger = self.simple_instance.logger
        log_level = "INFO"
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        trials = [ConnectionRefusedError()]*3 + [(reader, writer)]
        #trials = [ConnectionRefusedError(), (reader, writer)]
        mock_open_connection.mock.side_effect = trials
        start = QMASTER_TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY,
            host="gul",
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=21555,
        )
        retry_msg = QMASTER_TO_GRAPHITE_RETRY_MSG.format(host="gul")
        connected = QMASTER_TO_GRAPHITE_CONNECTED_MSG
        proto = [start] + [retry_msg]*3 + [connected]
        cn = self.simple_instance.__class__.__name__
        expected = ["{}:{}:{}".format(log_level, cn, _) for _ in proto]
        self.simple_instance._to_graphite_queue.get = AsyncioMock(
            side_effect=InventedException())
        with self.assertRaises(InventedException):
            with self.assertLogs(logger, level=log_level) as log:            
                asyncio_run(self.simple_instance._send_to_graphite())
        self.assertEqual(expected, log.output)


    # @patch("qulo.qmaster.convert_pickled_dict_to_graphite_format")
    # def test_send_to_graphite_calls_writer_write_with_correct_arg(
    #         self, mock_convert_pickled_dict_to_graphite_format):
    #     with patch(
    #             "qulo.qmaster.asyncio.open_connection", new=AsyncioMock()
    #             ) as open_connection:
    #         reader = MagicMock()
    #         writer = MagicMock()
    #         open_connection.mock.return_value = (reader, writer)
    #         self.simple_instance._to_graphite_queue = MagicMock()
    #         for num in 1,2,5:
    #             values = [MagicMock() for _ in range(num)] + [InventedException()]
    #             self.simple_instance._to_graphite_queue.get = AsyncioMock(side_effect=values)
    #             expected_calls = [call(value) for value in values[:-1]]
    #             with self.assertRaises(InventedException):
    #                 asyncio_run(self.simple_instance.send_to_graphite())
    #             writer.write.assert_has_calls(expected_calls)
    #             writer.write.reset_mock()

                
if __name__ == "__main__":
    unittest.main()

