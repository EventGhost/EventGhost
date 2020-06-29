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


TIMING = 527


class JVC(protocol_base.IrProtocolBase):
    """
    IR decoder for the JVC protocol.
    """
    irp = '{37.9k,527,lsb}<1,-1|1,-3>(16,-8,D:8,F:8,1,^59.08m,(D:8,F:8,1,^46.42m)*)'
    frequency = 37900
    bit_count = 16
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 59080]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = [TIMING, 46420]
    _repeat_bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _parameters = [
        ['D', 0, 7],
        ['F', 8, 15],
    ]
    # [D:0..255,F:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['function', 0, 255]
    ]

    def encode(self, device, function):
        encoded_dev = list(
            self._get_timing(device, i) for i in range(8)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )

        packet = self._build_packet(
            encoded_dev,
            encoded_func
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            8432, -4216, 527, -527, 527, -527, 527, -527, 527, -527, 527, -527, 527, -1581, 527, -527, 527, -1581,
            527, -527, 527, -527, 527, -527, 527, -527, 527, -527, 527, -1581, 527, -527, 527, -1581, 527, -24825
        ]]

        params = [dict(device=160, function=160)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=160, function=160)
        protocol_base.IrProtocolBase._test_encode(self, params)


JVC = JVC()
