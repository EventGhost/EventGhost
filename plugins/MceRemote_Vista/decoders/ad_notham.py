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

TIMING = 895


class AdNotham(protocol_base.IrProtocolBase):
    """
    IR decoder for the AdNotham protocol.
    """
    irp = '{35.7k,895,msb}<1,-1|-1,1>(1,-2,1,D:6,F:6,^114m)*'
    frequency = 35700
    bit_count = 12
    encoding = 'msb'

    _lead_in = [TIMING, -TIMING * 2, TIMING]
    _lead_out = [114000]
    _bursts = [[TIMING, -TIMING], [-TIMING,  TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 5],
        ['F', 6, 11],
    ]
    # [D:0..63,F:0..63]
    encode_parameters = [
        ['device', 0, 63],
        ['function', 0, 63],
    ]

    def encode(self, device, function):

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(6)),
            list(self._get_timing(function, i) for i in range(6))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            895, -1790, 1790, -895, 895, -895, 895, -1790, 895, -895, 895, -895, 1790, -1790, 895, -895,
            1790, -1790, 1790, -89835
        ]]

        params = [dict(device=7, function=26)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=7, function=26)
        protocol_base.IrProtocolBase._test_encode(self, params)


AdNotham = AdNotham()
