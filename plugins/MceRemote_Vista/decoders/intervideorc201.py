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


TIMING = 300


class InterVideoRC201(protocol_base.IrProtocolBase):
    """
    IR decoder for the InterVideoRC201 protocol.
    """
    irp = '{38k,300,lsb}<1,-1|1,-3>(10,-5,0:1,F:6,768:10,1,-10m)*'
    frequency = 38000
    bit_count = 17
    encoding = 'lsb'

    _lead_in = [TIMING * 10, -TIMING * 5]
    _lead_out = [TIMING, -10000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 5]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['F', 1, 6],
        ['C1', 7, 16],
    ]
    # [F:0..63]
    encode_parameters = [
        ['function', 0, 63],
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 0 or code.c1 != 768:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, function):
        c0 = 0
        c1 = 768

        encoded_c0 = list(
            self._get_timing(c0, i) for i in range(1)
        )
        encoded_c1 = list(
            self._get_timing(c1, i) for i in range(10)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(6)
        )
        packet = self._build_packet(
            encoded_c0,
            encoded_func,
            encoded_c1,
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3000, -1500, 300, -300, 300, -300, 300, -300, 300, -1500, 300, -300, 300, -300, 300, -1500, 300, -300,
            300, -300, 300, -300, 300, -300, 300, -300, 300, -300, 300, -300, 300, -300, 300, -1500, 300, -1500,
            300, -10000
        ]]

        params = [dict(function=36)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=36)
        protocol_base.IrProtocolBase._test_encode(self, params)


InterVideoRC201 = InterVideoRC201()
