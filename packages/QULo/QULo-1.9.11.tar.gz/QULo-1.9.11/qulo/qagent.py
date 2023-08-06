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

import asyncio
import pickle

from qulo.qulod import QuloD
from qulo.conf import QAgentConf
from qulo.constants import (
    PROTO_STARTING_PROGRAM_MSG, PROTO_STOPPED_PROGRAM_MSG, PROTO_CANT_STOP_MSG,
    START_STOP_ERROR, NOT_RUNNING_MESSAGE, QAGENT_PROGRAM, PROTO_MEASUREMENT_MSG,
    QAGENT_TO_QMASTER_DATA_PORT_KEY, QMASTER_HOST_KEY,
    QAGENT_TO_QMASTER_CONNECTING_MSG, QAGENT_TO_QMASTER_CONNECTED_MSG,
)
from qulo.maind import generic_main


QAGENT_STARTING_MESSAGE = PROTO_STARTING_PROGRAM_MSG.format(program=QAGENT_PROGRAM)
QAGENT_STOP_MESSAGE = PROTO_STOPPED_PROGRAM_MSG.format(program=QAGENT_PROGRAM)
QAGENT_CANT_STOP_MESSAGE = PROTO_CANT_STOP_MSG.format(program=QAGENT_PROGRAM)


class QAgent(QuloD):
    _starting_message = QAGENT_STARTING_MESSAGE
    _stopped_message = QAGENT_STOP_MESSAGE
    _cant_stop_message = QAGENT_CANT_STOP_MESSAGE

    def __init__(self, conf):
        super().__init__(conf)
        self._sensors_queue = asyncio.Queue()
        self._to_master_queue = asyncio.Queue()
        
    @property
    def sensors(self):
        return self._conf.sensors
    
    def run(self):
        for sensor in self.sensors:
            self.submit_task(sensor, self._sensors_queue)
        self.submit_task(self.report_data)
        self.submit_task(self.send_to_master)
        super().run()

    async def report_data(self):
        while True:
            value = await self._sensors_queue.get()
            self.logger.debug(PROTO_MEASUREMENT_MSG.format(value))
            await self._to_master_queue.put(pickle.dumps(value))
            
    async def send_to_master(self):
        host = self._conf.qmaster[QMASTER_HOST_KEY]
        port = self._conf.qmaster[QAGENT_TO_QMASTER_DATA_PORT_KEY]
        self.logger.info(
            QAGENT_TO_QMASTER_CONNECTING_MSG.format(
                host_key=QMASTER_HOST_KEY, host=host,
                port_key=QAGENT_TO_QMASTER_DATA_PORT_KEY, port=port,
            )
        )
        reader, writer = await asyncio.open_connection(
            host, port, loop=self._event_loop,
        )
        self.logger.info(QAGENT_TO_QMASTER_CONNECTED_MSG)
        while True:
            message = await self._to_master_queue.get()
            writer.write(message)
        #writer.close()# not needed (?) review the protocol; is this correct?
        #              # I think I should factorize this functionality in a client class

def main():
    generic_main(QAgentConf, QAgent)
