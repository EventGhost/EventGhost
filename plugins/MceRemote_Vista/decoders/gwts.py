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


TIMING = 417

# TODO: finish


class GwtS(protocol_base.IrProtocolBase):
    """
    IR decoder for the GwtS protocol.
    """
    irp = '{38.005k,417,lsb}<1|-1>(0:1,D:8,1:2,F:8,1:2,CRC:8,1:1)'
    frequency = 38005
    bit_count = 30
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING, 108000]
    _middle_timings = []
    _bursts = [[TIMING, 0], [0, -TIMING]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 8]
    _repeat_lead_out = [TIMING, 108000]
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['D', 1, 8],
        ['C1', 9, 10],
        ['F', 11, 18],
        ['C2', 19, 20],
        ['CRC', 21, 28],
        ['C3', 29, 29]
    ]
    # [D:0..255=144,F:0..255,CRC:0..255]
    encode_parameters = [
        # ['device', 0, 255],
        # ['function', 0, 255],
        # ['crc', 0, 255]
    ]

    def decode(self, data, frequency=0):
        raise DecodeError
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 0 or code.c1 != 1 or code.c2 != 1 or code.c3 != 1:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function, crc):
        c0 = 0
        c1 = 1
        c2 = 1
        c3 = 1

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(7)),
            list(self._get_timing(c1, i) for i in range(2)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(c2, i) for i in range(2)),
            list(self._get_timing(crc, i) for i in range(8)),
            list(self._get_timing(c3, i) for i in range(1)),
        )

        return [packet]

    def _test_decode(self):
        return
        rlc = [[
            417, -1251, 834, -417, 834, -417, 1251, -834, 1668, -417, 417, -834, 417, -417, 834, -417, 417, -417
        ]]

        params = [dict(device=39, e=247, function=12, crc=75)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        return
        params = dict(device=84, e=247, function=1, sub_device=225)
        protocol_base.IrProtocolBase._test_encode(self, params)


GwtS = GwtS()


