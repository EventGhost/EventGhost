# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

# Local imports
from . import protocol_base


TIMING = 315


class Bryston(protocol_base.IrProtocolBase):
    """
    IR decoder for the Bryston protocol.
    """
    irp = '{38.0k,315,lsb}<1,-6|6,-1>(D:10,F:8,-18m)*'
    frequency = 38000
    bit_count = 18
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [-18000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 6], [TIMING * 6, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 9],
        ['F', 10, 17]
    ]
    # [D:0..1023,F:0..255]
    encode_parameters = [
        ['device', 0, 1023],
        ['function', 0, 255],
    ]

    def encode(self, device, function):

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(10)),
            list(self._get_timing(function, i) for i in range(8))
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            1890, -315, 315, -1890, 1890, -315, 315, -1890, 315, -1890, 315, -1890, 1890, -315,
            315, -1890, 315, -1890, 1890, -315, 1890, -315, 1890, -315, 1890, -315, 1890, -315,
            1890, -315, 315, -1890, 315, -1890, 1890, -18315,
        ]]

        params = [dict(device=581, function=159)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=581, function=159)
        protocol_base.IrProtocolBase._test_encode(self, params)


Bryston = Bryston()
