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


TIMING = 44


class Jerrold(protocol_base.IrProtocolBase):
    """
    IR decoder for the Jerrold protocol.
    """
    irp = '{0k,44,lsb}<1,-7.5m|1,-11.5m>(F:5,1,-23.5m)*'
    frequency = 0
    bit_count = 5
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING, -23500]
    _middle_timings = []
    _bursts = [[TIMING, -7500], [TIMING, -11500]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['F', 0, 4],
    ]
    # [F:0..31]
    encode_parameters = [
        ['function', 0, 31],
    ]

    def encode(self, function):
        encoded_func = list(
            self._get_timing(function, i) for i in range(5)
        )

        packet = self._build_packet(encoded_func)

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[44, -11500, 44, -7500, 44, -7500, 44, -11500, 44, -11500, 44, -23500]]

        params = [dict(function=25)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=25)
        protocol_base.IrProtocolBase._test_encode(self, params)


Jerrold = Jerrold()
