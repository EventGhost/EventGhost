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


class Kaseikyo(protocol_base.IrProtocolBase):
    """
    IR decoder for the Kaseikyo protocol.
    """
    irp = (
        '{37k,432,lsb}<1,-1|1,-3>(8,-4,M:8,N:8,X:4,D:4,S:8,F:8,E:4,C:4,1,-173)*'
        '{X=((M^N)::4)^(M^N),chksum=D^S^F^(E*16),C=chksum::4^chksum}'
    )
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
        ['M', 0, 7],
        ['N', 8, 15],
        ['X', 16, 19],
        ['D', 20, 23],
        ['S', 24, 31],
        ['F', 32, 39],
        ['E', 40, 43],
        ['CHECKSUM', 44, 47]
    ]
    # [D:0..15,S:0..255,F:0..255,E:0..15,M:0..255,N:0..255]
    encode_parameters = [
        ['device', 0, 15],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['extended_function', 0, 15],
        ['mode', 0, 255],
        ['n', 0, 255]
    ]

    def _calc_checksum(self, mode, n, device, sub_device, function, extended_function):
        x = ((mode ^ n) >> 4) ^ (mode ^ n)
        checksum = device ^ sub_device ^ function ^ (extended_function * 16)
        checksum = checksum >> 4 ^ checksum

        return self._get_bits(x, 0, 3), self._get_bits(checksum, 0, 3)

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        x, checksum = self._calc_checksum(
            code.mode,
            code.n,
            code.device,
            code.sub_device,
            code.function,
            code.extended_function
        )

        if x != code.x or checksum != code.checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, mode, n, device, sub_device, function, extended_function):
        x, checksum = self._calc_checksum(
            mode, n, device, sub_device, function, extended_function
        )

        encoded_mode = list(
            self._get_timing(mode, i) for i in range(8)
        )
        encoded_n = list(
            self._get_timing(n, i) for i in range(8)
        )

        encoded_x = list(
            self._get_timing(x, i) for i in range(4)
        )

        encoded_dev = list(
            self._get_timing(device, i) for i in range(4)
        )
        encoded_sub = list(
            self._get_timing(sub_device, i) for i in range(8)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )
        encoded_ex_func = list(
            self._get_timing(extended_function, i) for i in range(4)
        )

        encoded_checksum = list(
            self._get_timing(checksum, i) for i in range(4)
        )

        packet = self._build_packet(
            encoded_mode,
            encoded_n,
            encoded_x,
            encoded_dev,
            encoded_sub,
            encoded_func,
            encoded_ex_func,
            encoded_checksum
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3456, -1728, 432, -1296, 432, -432, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -1296,
            432, -1296, 432, -432, 432, -432, 432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -1296,
            432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -432, 432, -1296,
            432, -432, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -1296,
            432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -1296, 432, -1296, 432, -432,
            432, -1296, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -1296, 432, -1296, 432, -74736
        ]]

        params = [dict(device=5, extended_function=14, function=192, mode=217, n=244, sub_device=131)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=5, extended_function=14, function=192, mode=217, n=244, sub_device=131)
        protocol_base.IrProtocolBase._test_encode(self, params)


Kaseikyo = Kaseikyo()
