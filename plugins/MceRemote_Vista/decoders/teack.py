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


TIMING = 432


class TeacK(protocol_base.IrProtocolBase):
    """
    IR decoder for the TeacK protocol.
    """
    irp = (
        '{37k,432,lsb}<1,-1|1,-3>(8,-4,67:8,83:8,X:4,D:4,S:8,F:8,T:8,1,-100,(8,-8,1,-100)*)'
        '{T=D+S:4:0+S:4:4+F:4:0+F:4:4}'
    )
    frequency = 37000
    bit_count = 48
    encoding = 'lsb'

    _lead_in = [TIMING * 8, -TIMING * 4]
    _lead_out = [TIMING, -TIMING * 100]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = [TIMING * 8, -TIMING * 8]
    _repeat_lead_out = [TIMING, -TIMING * 100]
    _repeat_bursts = []

    # 67:8,83:8,X:4,D:4,S:8,F:8,T:8
    _parameters = [
        ['C0', 0, 7],
        ['C1', 8, 15],
        ['X', 16, 19],
        ['D', 20, 23],
        ['S', 24, 31],
        ['F', 32, 39],
        ['CHECKSUM', 40, 47]
    ]
    # [D:0..15,S:0..255,F:0..255,X:0..15=1]
    encode_parameters = [
        ['device', 0, 15],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['x', 0, 15]
    ]

    def _calc_checksum(self, device, sub_device, function):
        f1 = self._get_bits(function, 0, 3)
        f2 = self._get_bits(function, 4, 7)
        s1 = self._get_bits(sub_device, 0, 3)
        s2 = self._get_bits(sub_device, 4, 7)
        return device + s1 + s2 + f1 + f2

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.device, code.sub_device, code.function)

        if code.c0 != 67 or code.c1 != 83 or code.checksum != checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function, x):
        c0 = 67
        c1 = 83

        checksum = self._calc_checksum(
            device,
            sub_device,
            function
        )

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(8)),
            list(self._get_timing(c1, i) for i in range(8)),
            list(self._get_timing(x, i) for i in range(4)),
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(checksum, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            3456, -1728, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432, 432, -432, 
            432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -1296, 
            432, -432, 432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -1296, 
            432, -432, 432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 
            432, -1296, 432, -1296, 432, -432, 432, -432, 432, -1296, 432, -1296, 432, -1296, 
            432, -432, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432, 
            432, -1296, 432, -432, 432, -1296, 432, -432, 432, -1296, 432, -432, 432, -432, 
            432, -43200, 
        ]]

        params = [dict(function=51, sub_device=159, device=12, x=11)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=51, sub_device=159, device=12, x=11)
        protocol_base.IrProtocolBase._test_encode(self, params)


TeacK = TeacK()
