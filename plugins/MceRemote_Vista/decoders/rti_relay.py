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


TIMING = 398


class RTIRelay(protocol_base.IrProtocolBase):
    """
    IR decoder for the RTIRelay protocol.
    """
    irp = '{40.244k,398,msb}<1,-1|-1,1>(1,A:31,F:1,F:8,D:23,D:8,0:4,-19.5m)*{A=0x7fe08080}'
    frequency = 40244
    bit_count = 75
    encoding = 'msb'

    _lead_in = [TIMING]
    _lead_out = [-19500]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [-TIMING, TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['A', 0, 30],
        ['F', 31, 31],
        ['F1', 32, 39],
        ['D1', 40, 62],
        ['D', 63, 70],
        ['C0', 71, 74]
    ]
    # [F:0..1,D:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['function', 0, 1],
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.a != 0x7FE08080 or code.c0 != 0:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        a = 0x7FE08080
        c0 = 0
        f1 = 0
        d1 = 0

        packet = self._build_packet(
            list(self._get_timing(a, i) for i in range(31)),
            list(self._get_timing(function, i) for i in range(1)),
            list(self._get_timing(f1, i) for i in range(8)),
            list(self._get_timing(d1, i) for i in range(23)),
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(c0, i) for i in range(4)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 
            398, -398, 398, -398, 796, -398, 398, -398, 398, -398, 398, -398, 398, -796, 796, -398, 
            398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 398, -796, 796, -398, 398, -398, 
            398, -398, 398, -398, 398, -398, 398, -398, 398, -796, 796, -398, 398, -398, 398, -398, 
            398, -398, 398, -398, 398, -398, 398, -796, 796, -398, 398, -398, 398, -398, 398, -398, 
            398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 398, -398, 
            398, -398, 398, -398, 398, -398, 398, -398, 398, -796, 398, -398, 398, -398, 796, -398, 
            398, -796, 796, -398, 398, -796, 398, -398, 398, -398, 796, -398, 398, -796, 796, -398, 
            398, -398, 398, -398, 398, -19898, 
        ]]

        params = [dict(device=57, function=1)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=57, function=1)
        protocol_base.IrProtocolBase._test_encode(self, params)


RTIRelay = RTIRelay()
