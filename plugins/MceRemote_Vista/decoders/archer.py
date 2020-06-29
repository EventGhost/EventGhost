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


TIMING = 12


class Archer(protocol_base.IrProtocolBase):
    """
    IR decoder for the Archer protocol.
    """
    irp = '{0k,12,lsb}<1,-3.3m|1,-4.7m>(F:5,1,-9.7m)*'
    frequency = 0
    bit_count = 5
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING, -9700]
    _bursts = [[TIMING, -3300], [TIMING, -4700]]

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
        packet = self._build_packet(
            list(self._get_timing(function, i) for i in range(5))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[12, -3300, 12, -3300, 12, -4700, 12, -4700, 12, -4700, 12, -9700]]

        params = [dict(function=28)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=28)
        protocol_base.IrProtocolBase._test_encode(self, params)


Archer = Archer()
