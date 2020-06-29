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


TIMING = 264


class Sharp(protocol_base.IrProtocolBase):
    """
    IR decoder for the Sharp protocol.
    """
    irp = '{38k,264,lsb}<1,-3|1,-7>(D:5,F:8,1:2,1,-165,D:5,~F:8,2:2,1,-165)*'
    frequency = 38000
    bit_count = 30
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING,  -TIMING * 165]
    _middle_timings = [(TIMING,  -TIMING * 165)]
    _bursts = [[TIMING, -TIMING * 3], [TIMING, -TIMING * 7]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 4],
        ['F', 5, 12],
        ['C0', 13, 14],
        ['D_CHECKSUM', 15, 19],
        ['F_CHECKSUM', 20, 27],
        ['C1', 28, 29]
    ]
    # [D:0..31,F:0..255]
    encode_parameters = [
        ['device', 0, 31],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, function):
        f = self._invert_bits(function, 8)
        return f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        if code.c0 != 1 or code.c1 != 2:
            raise DecodeError('Checksum failed')

        f_checksum = self._calc_checksum(code.function)

        if code.device != code.d_checksum or f_checksum != code.f_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        func_checksum = self._calc_checksum(function)
        c0 = 1
        c1 = 2

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(5)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(c0, i) for i in range(2)),
            self._middle_timings,
            list(self._get_timing(device, i) for i in range(5)),
            list(self._get_timing(func_checksum, i) for i in range(8)),
            list(self._get_timing(c1, i) for i in range(2))
        )

        return [packet]

    def _test_decode(self):
        rlc = [
            [
                +264, -792, +264, -792, +264, -792, +264, -1848, +264, -792, +264, -792, +264, -792, +264, -792, +264,
                -792, +264, -1848, +264, -792, +264, -1848, +264, -1848, +264, -1848, +264, -792, +264, -43560, +264,
                -792, +264, -792, +264, -792, +264, -1848, +264, -792, +264, -1848, +264, -1848, +264, -1848, +264,
                -1848, +264, -792, +264, -1848, +264, -792, +264, -792, +264, -792, +264, -1848, +264, -43560
            ]
        ]

        params = [dict(device=8, function=208)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=8, function=208)
        protocol_base.IrProtocolBase._test_encode(self, params)


Sharp = Sharp()
5, 6, 9, 14