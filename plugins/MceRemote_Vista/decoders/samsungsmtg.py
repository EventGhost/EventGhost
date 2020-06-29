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


TIMING = 497


class SamsungSMTG(protocol_base.IrProtocolBase):
    """
    IR decoder for the SamsungSMTG protocol.
    """
    irp = '{38.5k,497,msb}<1,-1|1,-3>(4497u,-4497u,D:16,1,-4497u,S:4,F:16,1,^120m)*'
    frequency = 38500
    bit_count = 36
    encoding = 'msb'

    _lead_in = [4497, -4497]
    _lead_out = [TIMING, 120000]
    _middle_timings = [(TIMING, -4497)]
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 15],
        ['S', 16, 19],
        ['F', 20, 35]
    ]
    # [D:0..65335,S:0..15,F:0..65535]
    encode_parameters = [
        ['device', 0, 65335],
        ['sub_device', 0, 15],
        ['function', 0, 65335],
    ]

    def encode(self, device, sub_device, function):

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(16)),
            self._middle_timings,
            list(self._get_timing(sub_device, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(16))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            4497, -4497, 497, -1491, 497, -1491, 497, -1491, 497, -497, 497, -1491, 497, -497,
            497, -1491, 497, -497, 497, -1491, 497, -497, 497, -1491, 497, -497, 497, -497,
            497, -1491, 497, -497, 497, -1491, 497, -4497, 497, -1491, 497, -1491, 497, -1491,
            497, -1491, 497, -497, 497, -1491, 497, -497, 497, -1491, 497, -497, 497, -497,
            497, -1491, 497, -1491, 497, -1491, 497, -497, 497, -497, 497, -497, 497, -497,
            497, -1491, 497, -1491, 497, -1491, 497, -48857,
        ]]

        params = [dict(device=60069, function=21383, sub_device=15)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=60069, function=21383, sub_device=15)
        protocol_base.IrProtocolBase._test_encode(self, params)


SamsungSMTG = SamsungSMTG()
