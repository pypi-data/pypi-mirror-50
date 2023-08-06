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

import pickle
import struct


class QMessage:
    """The QMessage class packs functionality to interact with messages produced in
    the sensors.
    """
    def __init__(self, message):
        self._message = pickle.loads(message)

    def to_graphite(self):
        data = self._arrange_for_graphite()
        dressed_message = self._pack_for_graphite(data)
        return dressed_message
    
    def _arrange_for_graphite(self):
        output_data = []
        basepath = "{}.{}".format(self._message["host"], self._message["sensor"])
        timestamp = self._message["time"]
        for k, v in self._message["value"].items():
            path = "{}.{}".format(basepath, k)
            output_data.append((path, (timestamp, v)))
        return output_data

    def _pack_for_graphite(self, in_data):
        payload = pickle.dumps(in_data, protocol=2)
        header = struct.pack("!L", len(payload))
        message_out = header + payload
        return message_out
