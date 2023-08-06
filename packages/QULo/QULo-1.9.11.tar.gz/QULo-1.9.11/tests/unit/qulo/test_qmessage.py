#!/bin/env python3

#######################################################################
# Copyright (C) 2018 David Palao
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
from unittest.mock import patch, MagicMock
import pickle

from qulo.qmessage import QMessage


class QMessageTestCase(unittest.TestCase):
    def make_qmessage(self, in_msg):
        pickled_message = pickle.dumps(in_msg)
        test_qmsg = QMessage(pickled_message)
        return test_qmsg
        
    @patch("qulo.qmessage.pickle.loads")
    def test_instance_sets_message_attribute(self, mock_loads):
        raw_test_message = "Winnipeg viene"
        loadsed_message = MagicMock()
        def _loads(arg):
            if arg == raw_test_message:
                return loadsed_message
            else:
                return None
        mock_loads.side_effect = _loads
        #
        qmsg = QMessage(raw_test_message)
        #
        self.assertEqual(qmsg._message, loadsed_message)

    @patch("qulo.qmessage.QMessage._pack_for_graphite")
    @patch("qulo.qmessage.QMessage._arrange_for_graphite")
    def test_to_graphite_arranges_and_packs_data_for_graphite(
            self,
            mock_arrange_for_graphite,
            mock_pack_for_graphite):
        test_data = MagicMock()
        expected_return = MagicMock()
        def mock_pack_for_graphite_side_effect(value):
            if value == test_data:
                return expected_return
        mock_arrange_for_graphite.return_value = test_data
        mock_pack_for_graphite.side_effect = mock_pack_for_graphite_side_effect
        test_qmsg = self.make_qmessage("Winnipeg vuelve")
        #
        result = test_qmsg.to_graphite()
        #
        self.assertEqual(result, expected_return)

    def test_arrange_for_graphite_return_value(self):
        values = {"0": 32, "winimo": 11, "jatemate": "3"}
        original_message = {
            "host": "machupichu",
            "sensor": "cochambrosidad",
            "time": "1843219764.8351722",
            "value": values,
        }
        prepath = "{host}.{sensor}".format(**original_message)
        timestamp = original_message["time"]
        expected = [
            ("{}.{}".format(prepath, k), (timestamp, v)) for k,v in values.items()
        ]
        test_qmsg = self.make_qmessage(original_message)
        result = test_qmsg._arrange_for_graphite()
        self.assertEqual(result, expected)

    def test_pack_for_graphite_returns_expected_data(self):
        in_data = "caca de vaca"
        import struct
        test_qmsg = self.make_qmessage("Winnipeg no me gusta")
        result = test_qmsg._pack_for_graphite(in_data)
        header = result[:4]
        payload = result[4:]
        self.assertEqual(in_data, pickle.loads(payload))
        self.assertEqual(
            struct.unpack("!L", header)[0],
            len(pickle.dumps(in_data, protocol=2))
        )
