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


# 432, -1296, 1
# 432, -432, 0
# 432, -1296,1
# 432, -432, 0
# 432, -432, 0
# 432, -1296, 1
# 432, -432, 0
# 432, -432 0

class DenonK(protocol_base.IrProtocolBase):
    """
    IR decoder for the DenonK protocol.
    """
    irp = '{37k,432,lsb}<1,-1|1,-3>(8,-4,84:8,50:8,0:4,D:4,S:4,F:12,((D*16)^S^(F*16)^(F:8:4)):8,1,-173)*'
    frequency = 37000
    bit_count = 48
    encoding = 'lsb'

    _lead_in = [TIMING * 8, -TIMING * 4]
    _lead_out = [TIMING, -TIMING * 173]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 7],
        ['C1', 8, 15],
        ['C2', 16, 19],
        ['D', 20, 23],
        ['S', 24, 27],
        ['F', 28, 39],
        ['CHECKSUM', 40, 47]
    ]
    # [D:0..15,S:0..15,F:0..4095]
    encode_parameters = [
        ['device', 0, 15],
        ['sub_device', 0, 15],
        ['function', 0, 4095],
    ]

    def _calc_checksum(self, device, sub_device, function):
        # ((D*16)^S^(F*16)^(F:8:4))
        d = device * 16
        f1 = function * 16
        f2 = self._get_bits(function, 3, 10)

        c = d ^ sub_device ^ f1 ^ f2
        c = self._get_bits(c, 0, 7)
        return c

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.device, code.sub_device, code.function)

        if code.c0 != 84 or code.c1 != 50 or code.c2 != 0:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function):
        c0 = 84
        c1 = 50
        c2 = 0
        checksum = self._calc_checksum(device, sub_device, function)

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(8)),
            list(self._get_timing(c1, i) for i in range(8)),
            list(self._get_timing(c2, i) for i in range(4)),
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(sub_device, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(12)),
            list(self._get_timing(checksum, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            3456, -1728, 432, -432, 432, -432, 432, -1296, 432, -432, 432, -1296, 432, -432, 432, -1296, 432, -432,
            432, -432, 432, -1296, 432, -432, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432,
            432, -432, 432, -432, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -1296, 432, -432,
            432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432,
            432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432, 432, -1296, 432, -432, 432, -1296, 432, -432,
            432, -432, 432, -1296, 432, -432, 432, -432, 432, -74736
        ]]

        params = [dict(device=3, function=384, sub_device=13)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=3, function=384, sub_device=13)
        protocol_base.IrProtocolBase._test_encode(self, params)


DenonK = DenonK()
