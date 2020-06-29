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


TIMING = 268

#  [[
#  1876, -1608,
#  804,
#
#  -268, 268, -268, 268, 268, -268, -268, 268, 268, -268, 268, -268, -268, 268, 268, -268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, 268, -268, -268, 268, -268, 268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, -268, 268, -268, 268, -268, 268, 268
#  -268, 268, -268, 268, 268, -268, -268, 268, 268, -268, 268, -268, -268, 268, 268, -268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, 268, -268, -268, 268, -268, 268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, -268, 268, -268, 268, -268, 268, 268,-268
#
#  -79268
#         ]]


class Amino(protocol_base.IrProtocolBase):
    """
    IR decoder for the Amino protocol.
    """
    irp = (
        '{37.3k,268,msb}<-1,1|1,-1>([T=1][T=0],7,-6,3,D:4,1:1,T:1,1:2,0:8,F:8,15:4,C:4,-79m)+'
        '{C=(D:4+4*T+9+F:4+F:4:4+15)&15}'
    )
    frequency = 37300
    bit_count = 32
    encoding = 'msb'

    _lead_in = [TIMING * 7, -TIMING * 6, TIMING * 3]
    _lead_out = [-79000]
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 3],
        ['C0', 4, 4],  # 1
        ['T', 5, 5],
        ['C1', 6, 7],  # 1
        ['C2', 8, 15],  # 0
        ['F', 16, 23],
        ['C3', 24, 27],  # 15
        ['CHECKSUM', 28, 31]
    ]
    # [D:0..15,F:0..255]
    encode_parameters = [
        ['device', 0, 15],
        ['function', 0, 255],
        ['toggle', 0, 1]
    ]

    def _calc_checksum(self, device, function, toggle, c3):
        d = self._get_bits(device, 0, 3)
        f1 = self._get_bits(function, 0, 3)
        f2 = self._get_bits(function, 4, 7)

        # (D:4+4*T+9+F:4+F:4:4+15)&15}
        return (d + 4 * toggle + 9 + f1 + f2 + c3) & c3

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.device, code.function, code.toggle, code.c3)

        if checksum != code.checksum or code.c0 != 1 or code.c1 != 1 or code.c2 != 0:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function, toggle):
        c0 = 1
        c1 = 1
        c2 = 0
        c3 = 15

        checksum = self._calc_checksum(
            device,
            function,
            toggle,
            c3
        )

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(c1, i) for i in range(2)),
            list(self._get_timing(c2, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(c3, i) for i in range(4)),
            list(self._get_timing(checksum, i) for i in range(4))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            1876, -1608, 804, -268, 268, -268, 536, -536, 536, -268, 268, -536, 536, -536, 268, -268,
            268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 536, -536,
            268, -268, 536, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268,
            268, -536, 268, -268, 268, -268, 536, -79268
        ]]

        params = [dict(device=2, function=79)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=2, function=79)
        protocol_base.IrProtocolBase._test_encode(self, params)


Amino = Amino()

