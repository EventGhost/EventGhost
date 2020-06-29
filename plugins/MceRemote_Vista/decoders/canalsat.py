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


TIMING = 250


class CanalSat(protocol_base.IrProtocolBase):
    """
    IR decoder for the CanalSat protocol.
    """
    irp = '{55.5k,250,msb}<-1,1|1,-1>(T=0,(1,-1,D:7,S:6,T:1,0:1,F:7,-89m,T=1)+)'
    frequency = 55500
    bit_count = 22
    encoding = 'msb'

    _lead_in = [TIMING, -TIMING]
    _lead_out = [-89000]
    _middle_timings = []
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 6],
        ['S', 7, 12],
        ['T', 13, 13],
        ['C0', 14, 14],
        ['F', 15, 21],
    ]
    # [D:0..127,S:0..63,F:0..127]
    encode_parameters = [
        ['device', 0, 127],
        ['sub_device', 0, 62],
        ['function', 0, 127],
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 0:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function):
        toggle = 0
        c0 = 0

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(7)),
            list(self._get_timing(sub_device, i) for i in range(6)),
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(7)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            250, -500, 250, -250, 250, -250, 250, -250, 250, -250, 500, -250, 250, -250, 250, -250,
            250, -500, 500, -500, 250, -250, 250, -250, 250, -250, 500, -250, 250, -250, 250, -250,
            250, -250, 250, -250, 250, -500, 250, -89000,
        ]]

        params = [dict(device=3, function=126, sub_device=52)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=3, function=126, sub_device=52)
        protocol_base.IrProtocolBase._test_encode(self, params)


CanalSat = CanalSat()
