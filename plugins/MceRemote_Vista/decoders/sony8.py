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


TIMING = 600


class Sony8(protocol_base.IrProtocolBase):
    """
    IR decoder for the Sony8 protocol.
    """
    irp = '{40k,600,lsb}<1,-1|2,-1>(4,-1,F:8,^45m)'
    frequency = 40000
    bit_count = 8
    encoding = 'lsb'

    _lead_in = [TIMING * 4, -TIMING]
    _lead_out = [45000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING * 2, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['F', 0, 7],
    ]
    # [F:0..255]
    encode_parameters = [
        ['function', 0, 255],
    ]

    def encode(self, function):

        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )

        packet = self._build_packet(encoded_func)

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            2400, -600, 1200, -600, 600, -600, 600, -600, 1200, -600, 600, -600, 600, -600,
            1200, -600, 600, -31200,
        ]]

        params = [dict(function=73)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=73)
        protocol_base.IrProtocolBase._test_encode(self, params)


Sony8 = Sony8()
