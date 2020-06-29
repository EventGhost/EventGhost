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


TIMING = 10


class Barco(protocol_base.IrProtocolBase):
    """
    IR decoder for the Barco protocol.
    """
    irp = '{0k,10,lsb}<1,-5|1,-15>(1,-25,D:5,F:6,1,-25,1,120m)+ '
    frequency = 0
    bit_count = 11
    encoding = 'lsb'

    _lead_in = [TIMING, -TIMING * 25]
    _lead_out = [TIMING, -TIMING * 25, TIMING, -120000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 5], [TIMING, -TIMING * 15]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 4],
        ['F', 5, 10],
    ]
    # [D:0..31,F:0..63]
    encode_parameters = [
        ['device', 0, 31],
        ['function', 0, 63],
    ]

    def encode(self, device, function, ):
        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(5)),
            list(self._get_timing(function, i) for i in range(6)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            10, -250, 10, -50, 10, -50, 10, -50, 10, -50, 10, -150, 10, -50, 10, -50, 10, -150, 10, -150, 10, -50,
            10, -150, 10, -250, 10, -120000
        ]]

        params = [dict(device=16, function=44)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=16, function=44)
        protocol_base.IrProtocolBase._test_encode(self, params)


Barco = Barco()

