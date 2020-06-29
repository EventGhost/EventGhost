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


TIMING = 444


class Entone(protocol_base.IrProtocolBase):
    """
    IR decoder for the Entone protocol.
    """
    irp = '{36k,444,msb}<-1,1|1,-1>(6,-2,1:1,M:3,<-2,2|2,-2>(T:1),0xE60396FFFFF:44,F:8,0:4,-131.0m)*{M=6,T=0}'
    frequency = 36000
    bit_count = 61
    encoding = 'msb'

    _lead_in = [TIMING * 6, -TIMING * 2]
    _lead_out = [-131000]
    _middle_timings = [{'start': 4, 'stop': 5, 'bursts': [[-TIMING * 2, TIMING * 2], [TIMING * 2, -TIMING * 2]]}]
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 8]
    _repeat_lead_out = [TIMING, 108000]
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['M', 1, 3],
        ['T', 4, 4],
        ['C1', 5, 48],
        ['F', 49, 56],
        ['C2', 57, 60]
    ]
    # [F:0..255]
    encode_parameters = [
        ['function', 0, 255]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 1 or code.mode != 6 or code.c1 != 0xE60396FFFFF or code.c2 != 0:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, function):
        c0 = 1
        c1 = 0xE60396FFFFF
        c2 = 0
        toggle = 0
        mode = 6

        toggle = self._middle_timings[0]['bursts'][toggle]

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(mode, i) for i in range(3)),
            toggle,
            list(self._get_timing(c1, i) for i in range(44)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(c2, i) for i in range(4)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            2664, -888, 444, -444, 444, -444, 444, -888, 444, -888, 1332, -444, 444, -444, 444, -888, 444, -444,
            888, -444, 444, -888, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 888, -444,
            444, -444, 444, -888, 444, -444, 888, -888, 888, -444, 444, -888, 888, -444, 444, -444, 444, -444,
            444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444,
            444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444,
            444, -444, 444, -888, 888, -444, 444, -444, 444, -888, 444, -444, 444, -444, 444, -444, 444, -444,
            444, -131000
        ]]

        params = [dict(function=238)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=238)
        protocol_base.IrProtocolBase._test_encode(self, params)


Entone = Entone()
