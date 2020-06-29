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


TIMING = 512


class Motorola(protocol_base.IrProtocolBase):
    """
    IR decoder for the Motorola protocol.
    """
    irp = '{32k,512,lsb}<-1,1|1,-1>(1,-5,1:1,F:7,D:2,^13.8m)*'
    frequency = 32000
    bit_count = 10
    encoding = 'lsb'

    _lead_in = [TIMING, -TIMING * 5]
    _lead_out = [13800]
    _middle_timings = []
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['F', 1, 7],
        ['D', 8, 9]
    ]
    # [D:0..4,F:0..127]
    encode_parameters = [
        ['device', 0, 4],
        ['function', 0, 127],
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 1:
            raise DecodeError('Invalid checksum')

        return code

    def encode(self, device, function):
        c0 = 1
        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(7)),
            list(self._get_timing(device, i) for i in range(2)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [
            [+512, -2560, +512, -512, +512, -1024, +1024, -512, +512, -1024, +1024, -1024, +512, -512, +1024, -1000]
        ]
        params = [dict(function=45, device=2)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=45, device=4)
        protocol_base.IrProtocolBase._test_encode(self, params)


Motorola = Motorola()
