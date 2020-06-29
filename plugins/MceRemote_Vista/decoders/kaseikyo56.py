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


class Kaseikyo56(protocol_base.IrProtocolBase):
    """
    IR decoder for the Kaseikyo56 protocol.
    """
    irp = (
        '{37k,432,lsb}<1,-1|1,-3>(8,-4,M:8,N:8,H:4,D:4,S:8,E:8,F:8,G:8,1,-173)*'
        '{H=((M^N)::4)^(M^N)'
    )
    frequency = 37000
    bit_count = 56
    encoding = 'lsb'

    _lead_in = [TIMING * 8, -TIMING * 4]
    _lead_out = [TIMING, -TIMING * 173]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['M', 0, 7],
        ['N', 8, 15],
        ['H', 16, 19],
        ['D', 20, 23],
        ['S', 24, 31],
        ['E', 32, 39],
        ['F', 40, 47],
        ['G', 48, 55]
    ]
    # [D:0..15,S:0..255,F:0..255,G:0..255,M:0..255,N:0..255,E:0..255]
    encode_parameters = [
        ['device', 0, 15],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['g', 0, 255],
        ['extended_function', 0, 15],
        ['mode', 0, 255],
        ['n', 0, 255]
    ]

    def _calc_checksum(self, mode, n):
        h = ((mode ^ n) >> 4) ^ (mode ^ n)
        return self._get_bits(h, 0, 3)

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        h = self._calc_checksum(
            code.mode,
            code.n
        )

        if h != code.h:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, mode, device, sub_device, function, extended_function, g, n):
        h = self._calc_checksum(mode, n)

        packet = self._build_packet(
            list(self._get_timing(mode, i) for i in range(8)),
            list(self._get_timing(n, i) for i in range(8)),
            list(self._get_timing(h, i) for i in range(4)),
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(extended_function, i) for i in range(8)),
            list(self._get_timing(g, i) for i in range(8))
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3456, -1728, 432, -1296, 432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -432,
            432, -432, 432, -1296, 432, -432, 432, -1296, 432, -432, 432, -432, 432, -1296, 432, -432,
            432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432, 432, -1296,
            432, -432, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -1296, 432, -432, 432, -1296,
            432, -432, 432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -1296,
            432, -432, 432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -1296, 432, -432,
            432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -432, 432, -1296, 432, -432,
            432, -1296, 432, -74736
        ]]

        params = [dict(device=4, extended_function=126, function=45, g=175, mode=59, n=165, sub_device=86)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=4, extended_function=126, function=45, g=175, mode=59, n=165, sub_device=86)
        protocol_base.IrProtocolBase._test_encode(self, params)


Kaseikyo56 = Kaseikyo56()
