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
from . import DecodeError


TIMING = 358


class Elunevision(protocol_base.IrProtocolBase):
    """
    IR decoder for the Elunevision protocol.
    """
    irp = '{0k,358,msb}<1,-3|3,-1>(10,-3,D:24,F:8,-7)*{D=0xf48080}'
    frequency = 0
    bit_count = 32
    encoding = 'msb'

    _lead_in = [TIMING * 10, -TIMING * 3]
    _lead_out = [-TIMING * 7]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 3], [TIMING * 3, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 23],
        ['F', 24, 31],
    ]
    # [F:0..255]
    encode_parameters = [
        ['function', 0, 255],
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.device != 0xF48080:
            raise DecodeError('Incorrect device')

        return code

    def encode(self, function):
        device = 0xF48080

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(24)),
            list(self._get_timing(function, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            3580, -1074, 1074, -358, 1074, -358, 1074, -358, 1074, -358, 358, -1074, 1074, -358, 358, -1074,
            358, -1074, 1074, -358, 358, -1074, 358, -1074, 358, -1074, 358, -1074, 358, -1074, 358, -1074,
            358, -1074, 1074, -358, 358, -1074, 358, -1074, 358, -1074, 358, -1074, 358, -1074, 358, -1074,
            358, -1074, 358, -1074, 1074, -358, 1074, -358, 358, -1074, 1074, -358, 1074, -358, 1074, -358,
            358, -3580
        ]]

        params = [dict(function=110)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=110)
        protocol_base.IrProtocolBase._test_encode(self, params)


Elunevision = Elunevision()
