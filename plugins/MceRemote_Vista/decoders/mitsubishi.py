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


class Mitsubishi(protocol_base.IrProtocolBase):
    """
    IR decoder for the Mitsubishi protocol.
    """
    irp = '{32.6k,300,lsb}<1,-3|1,-7>(D:8,F:8,1,-80)*'
    frequency = 32600
    bit_count = 16
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING, -TIMING * 80]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 3], [TIMING, -TIMING * 7]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['F', 8, 15],
    ]
    # [D:0..127,F:0..255]
    encode_parameters = [
        ['device', 0, 127],
        ['function', 0, 255],
    ]

    def encode(self, device, function):
        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8))
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            300, -2100, 300, -900, 300, -900, 300, -2100, 300, -900, 300, -2100, 300, -900,
            300, -900, 300, -2100, 300, -2100, 300, -2100, 300, -2100, 300, -2100, 300, -2100,
            300, -900, 300, -2100, 300, -24000,
        ]]

        params = [dict(device=41, function=191)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=41, function=191)
        protocol_base.IrProtocolBase._test_encode(self, params)


Mitsubishi = Mitsubishi()
