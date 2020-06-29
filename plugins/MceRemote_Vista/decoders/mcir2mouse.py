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


class MCIR2mouse(protocol_base.IrProtocolBase):
    """
    IR decoder for the MCIR2mouse protocol.
    """
    irp = '{0k,300,msb}<-1,1|1,-1>(9,8:8,C:5,y:7,x:7,R:1,L:1,F:5,-10.7m)*'
    frequency = 0
    bit_count = 34
    encoding = 'msb'

    _lead_in = [TIMING * 9]
    _lead_out = [-10700]
    _middle_timings = []
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 7],
        ['MIDDLE', 8, 12],
        ['Y', 13, 19],
        ['X', 20, 26],
        ['RIGHT', 27, 27],
        ['LEFT', 28, 28],
        ['F', 29, 33]
    ]
    # [C:0..31,L:0..1,R:0..1,x:0..127,y:0..127,F:0..31]
    encode_parameters = [
        ['middle', 0, 31],
        ['left', 0, 1],
        ['right', 0, 1],
        ['x', 0, 127],
        ['y', 0, 127],
        ['function', 0, 31]

    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 8:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, middle, left, right, x, y, function):
        c0 = 8

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(8)),
            list(self._get_timing(middle, i) for i in range(5)),
            list(self._get_timing(y, i) for i in range(7)),
            list(self._get_timing(x, i) for i in range(7)),
            list(self._get_timing(right, i) for i in range(1)),
            list(self._get_timing(left, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(5))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            2700, -300, 300, -300, 300, -300, 300, -300, 600, -600, 300, -300, 300, -300, 
            600, -300, 300, -300, 300, -300, 300, -600, 300, -300, 600, -300, 300, -600, 300, -300, 
            300, -300, 300, -300, 600, -600, 600, -300, 300, -300, 300, -600, 300, -300, 600, -300, 
            300, -600, 600, -600, 600, -600, 300, -10700, 
        ]]

        params = [dict(function=10, middle=30, right=1, y=48, x=92, left=1)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=10, middle=30, right=1, y=48, x=92, left=1)
        protocol_base.IrProtocolBase._test_encode(self, params)


MCIR2mouse = MCIR2mouse()
