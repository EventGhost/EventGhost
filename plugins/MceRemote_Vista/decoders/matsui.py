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


TIMING = 525


class Matsui(protocol_base.IrProtocolBase):
    """
    IR decoder for the Matsui protocol.
    """
    irp = '{38k,525,lsb}<1,-1|1,-3>(D:3,F:7,1,^30.5m)*'
    frequency = 38000
    bit_count = 10
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING, 30500]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 2],
        ['F', 3, 9],
    ]
    # [D:0..7,F:0..127]
    encode_parameters = [
        ['device', 0, 7],
        ['function', 0, 127],
    ]

    def encode(self, device, function):
        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(3)),
            list(self._get_timing(function, i) for i in range(7))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            525, -525, 525, -1575, 525, -525, 525, -1575, 525, -1575, 525, -525, 525, -525, 
            525, -1575, 525, -1575, 525, -1575, 525, -13175, 
        ]]

        params = [dict(device=2, function=115)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=2, function=115)
        protocol_base.IrProtocolBase._test_encode(self, params)


Matsui = Matsui()
