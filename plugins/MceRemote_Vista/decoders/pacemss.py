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


TIMING = 630


class PaceMSS(protocol_base.IrProtocolBase):
    """
    IR decoder for the PaceMSS protocol.
    """
    irp = '{38k,630,msb}<1,-7|1,-11>(1,-5,1,-5,T:1,D:1,F:8,1,^120m)*'
    frequency = 38000
    bit_count = 10
    encoding = 'msb'

    _lead_in = [TIMING, -TIMING * 5, TIMING, -TIMING * 5]
    _lead_out = [TIMING, 120000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 7], [TIMING, -TIMING * 11]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['T', 0, 0],
        ['D', 1, 1],
        ['F', 2, 9],
    ]
    # [D:0..1,F:0..255,T:0..1]
    encode_parameters = [
        ['device', 0, 1],
        ['function', 0, 255],
        ['toggle', 0, 1]
    ]

    def encode(self, device, function, toggle):
        packet = self._build_packet(
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            630, -3150, 630, -3150, 630, -4410, 630, -4410, 630, -6930, 630, -4410, 630, -4410,
            630, -6930, 630, -6930, 630, -4410, 630, -4410, 630, -4410, 630, -53850,
        ]]

        params = [dict(function=152, toggle=0, device=0)]
        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=152, toggle=0, device=0)
        protocol_base.IrProtocolBase._test_encode(self, params)


PaceMSS = PaceMSS()
