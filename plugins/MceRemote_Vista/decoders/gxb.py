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


TIMING = 520


class GXB(protocol_base.IrProtocolBase):
    """
    IR decoder for the GXB protocol.
    """
    irp = '{38.3k,520,msb}<1,-3|3,-1>(1,-1,D:4,F:8,P:1,1,^100m)*{P=1-#F%2}'
    frequency = 38300
    bit_count = 13
    encoding = 'msb'

    _lead_in = [TIMING, -TIMING]
    _lead_out = [TIMING, 100000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 3], [TIMING * 3, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 3],
        ['F', 4, 11],
        ['CHECKSUM', 12, 12],
    ]
    # [D:0..15,F:0..255]
    encode_parameters = [
        ['device', 0, 15],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, function):
        p = (1 - self._count_one_bits(function % 2)) % 2
        return int(not self._get_bit(p, 0))

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.function)

        if checksum != code.checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        checksum = self._calc_checksum(function)

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(checksum, i) for i in range(1)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            520, -520, 1560, -520, 1560, -520, 1560, -520, 520, -1560, 520, -1560, 1560, -520, 520, -1560,
            1560, -520, 520, -1560, 520, -1560, 1560, -520, 520, -1560, 520, -1560, 520, -71400
        ]]

        params = [dict(device=14, function=82)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=14, function=82)
        protocol_base.IrProtocolBase._test_encode(self, params)


GXB = GXB()
