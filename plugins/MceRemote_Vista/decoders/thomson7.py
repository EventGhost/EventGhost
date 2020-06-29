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


class Thomson7(protocol_base.IrProtocolBase):
    """
    IR decoder for the Thomson7 protocol.
    """
    irp = '{33k,500,lsb}<1,-4|1,-9>(D:4,(1-T):1,F:7,1,^80m)*'
    frequency = 33000
    bit_count = 12
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING, 80000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 4], [TIMING, -TIMING * 9]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    # D:4,(1-T):1,D:1:4,F:6
    _parameters = [
        ['D', 0, 3],
        ['T', 4, 4],
        ['F', 5, 11],
    ]
    # [D:0..31,F:0..127,T@:0..1=0]
    encode_parameters = [
        ['device', 0, 31],
        ['function', 0, 127],
        ['toggle', 0, 1]
    ]

    def encode(self, device, function, toggle):

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(7))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            500, -2000, 500, -2000, 500, -4500, 500, -2000, 500, -2000, 500, -2000, 500, -4500, 
            500, -2000, 500, -4500, 500, -2000, 500, -2000, 500, -2000, 500, -42000, 
        ]]

        params = [dict(function=10, toggle=0, device=4)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=10, toggle=0, device=4)
        protocol_base.IrProtocolBase._test_encode(self, params)


Thomson7 = Thomson7()
