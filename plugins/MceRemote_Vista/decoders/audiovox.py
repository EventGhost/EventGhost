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


TIMING = 500


class Audiovox(protocol_base.IrProtocolBase):
    """
    IR decoder for the Audiovox protocol.
    """
    irp = '{40k,500,lsb}<1,-1|1,-3>(16,-8,D:8,1,-8,F:8,1,-40)*'
    frequency = 40000
    bit_count = 16
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, -TIMING * 40]
    _middle_timings = [(TIMING, -TIMING * 8)]
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['F', 8, 15],
    ]
    # [D:0..255,F:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['function', 0, 255],
    ]

    def encode(self, device, function):
        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            self._middle_timings,
            list(self._get_timing(function, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            8000, -4000, 500, -1500, 500, -1500, 500, -500, 500, -500, 500, -500, 500, -1500,
            500, -1500, 500, -500, 500, -4000, 500, -500, 500, -500, 500, -1500, 500, -1500,
            500, -1500, 500, -1500, 500, -1500, 500, -1500, 500, -20000,
        ]]

        params = [dict(device=99, function=252)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=99, function=252)
        protocol_base.IrProtocolBase._test_encode(self, params)


Audiovox = Audiovox()
