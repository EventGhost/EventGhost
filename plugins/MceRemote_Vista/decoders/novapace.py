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


class NovaPace(protocol_base.IrProtocolBase):
    """
    IR decoder for the NovaPace protocol.
    """
    irp = '{38k,300,msb}<-1,1|1,-1>(1,-1,D:10,S:8,F:8,(1-T):1,-1,1,-82m)*'
    frequency = 38000
    bit_count = 27
    encoding = 'msb'

    _lead_in = [TIMING, -TIMING]
    _lead_out = [-TIMING, TIMING, -82000]
    _middle_timings = []
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 9],
        ['S', 10, 17],
        ['F', 18, 25],
        ['T', 26, 26]
    ]
    # [D:0..1023,S:0..255,F:0..255,T@:0..1=0]
    encode_parameters = [
        ['device', 0, 1023],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['toggle', 0, 1]
    ]

    def encode(self, device, sub_device, function, toggle):
        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(10)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(toggle, i) for i in range(1))
        )

        return packet

    def _test_decode(self):
        rlc = [[
            300, -600, 600, -600, 600, -600, 300, -300, 600, -300, 300, -300, 300, -300, 300, -600, 600, -600,
            300, -300, 600, -600, 300, -300, 300, -300, 600, -300, 300, -300, 300, -300, 300, -600, 300, -300,
            300, -300, 600, -300, 300, -600, 300, -82000
        ]]

        params = [dict(sub_device=72, function=241, toggle=1, device=335)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(sub_device=72, function=241, toggle=1, device=335)
        protocol_base.IrProtocolBase._test_encode(self, params)


NovaPace = NovaPace()
