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


TIMING = 15


class Revox(protocol_base.IrProtocolBase):
    """
    IR decoder for the Revox protocol.
    """
    irp = '{0k,15,lsb}<1,-9|1,-19>(1,-29,0:1,D:4,F:6,1,-29,1,-100285u)*'
    frequency = 0
    bit_count = 11
    encoding = 'lsb'

    _lead_in = [TIMING, -TIMING * 29]
    _lead_out = [TIMING, -TIMING * 29, TIMING, -100285]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 9], [TIMING, -TIMING * 19]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['D', 1, 4],
        ['F', 5, 10]
    ]
    # [D:0..15,F:0..63]
    encode_parameters = [
        ['device', 0, 15],
        ['function', 0, 63],
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 0:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        c0 = 0

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(6))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            15, -435, 15, -135, 15, -285, 15, -285, 15, -135, 15, -285, 15, -285, 15, -135, 
            15, -135, 15, -135, 15, -285, 15, -135, 15, -435, 15, -100285, 
        ]]

        params = [dict(device=11, function=17)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=11, function=17)
        protocol_base.IrProtocolBase._test_encode(self, params)


Revox = Revox()
