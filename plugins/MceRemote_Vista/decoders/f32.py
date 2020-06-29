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

TIMING = 422


class F32(protocol_base.IrProtocolBase):
    """
    IR decoder for the F32 protocol.
    """
    irp = '{37.9k,422,msb}<1,-3|3,-1>(D:8,S:8,F:8,E:8,-100m)*'
    frequency = 37900
    bit_count = 32
    encoding = 'msb'

    _lead_in = []
    _lead_out = [-100000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 3], [TIMING * 3, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['F', 16, 23],
        ['E', 24, 31]
    ]
    # [D:0..255,S:0..255,F:0..255,E:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['e', 0, 255]
    ]

    def encode(self, device, sub_device, function, e):

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(e, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            422, -1266, 422, -1266, 1266, -422, 1266, -422, 422, -1266, 422, -1266, 422, -1266, 422, -1266,
            1266, -422, 422, -1266, 422, -1266, 422, -1266, 1266, -422, 422, -1266, 422, -1266, 1266, -422,
            1266, -422, 1266, -422, 1266, -422, 1266, -422, 422, -1266, 422, -1266, 1266, -422, 1266, -422,
            422, -1266, 1266, -422, 1266, -422, 1266, -422, 422, -1266, 1266, -422, 1266, -422, 422, -101266
        ]]

        params = [dict(device=48, function=243, sub_device=137, e=118)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=48, function=243, sub_device=137, e=118)
        protocol_base.IrProtocolBase._test_encode(self, params)


F32 = F32()
