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


TIMING = 400


class SharpDVD(protocol_base.IrProtocolBase):
    """
    IR decoder for the SharpDVD protocol.
    """
    irp = '{38k,400,lsb}<1,-1|1,-3>(8,-4,170:8,90:8,15:4,D:4,S:8,F:8,E:4,C:4,1,-48)*{C=D^S:4:0^S:4:4^F:4:0^F:4:4^E:4}'
    frequency = 38000
    bit_count = 48
    encoding = 'lsb'

    _lead_in = [TIMING * 8, -TIMING * 4]
    _lead_out = [TIMING, -TIMING * 48]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []
    # 170:8,90:8,15:4,D:4,S:8,F:8,E:4,C:4
    _parameters = [
        ['C0', 0, 7],
        ['C1', 8, 15],
        ['C2', 16, 19],
        ['D', 20, 23],
        ['S', 24, 31],
        ['F', 32, 39],
        ['E', 40, 43],
        ['CHECKSUM', 44, 47]
    ]
    # [D:0..15,S:0..255,F:0..255,E:0..15=1]
    encode_parameters = [
        ['device', 0, 15],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['extended_function', 0, 15]
    ]

    def _calc_checksum(self, device, sub_device, function, extended_function):
        f1 = self._get_bits(function, 0, 3)
        f2 = self._get_bits(function, 4, 7)
        s1 = self._get_bits(sub_device, 0, 3)
        s2 = self._get_bits(sub_device, 4, 7)
        e = self._get_bits(extended_function, 0, 3)

        return device ^ s1 ^ s2 ^ f1 ^ f2 ^ e

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(
            code.device,
            code.sub_device,
            code.function,
            code.extended_function
        )

        if code.c0 != 170 or code.c1 != 90 or code.c2 != 15 or checksum != code.checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function, extended_function):
        checksum = self._calc_checksum(
            device,
            sub_device,
            function,
            extended_function
        )

        c0 = 170
        c1 = 90
        c2 = 15

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(8)),
            list(self._get_timing(c1, i) for i in range(8)),
            list(self._get_timing(c2, i) for i in range(4)),
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(extended_function, i) for i in range(4)),
            list(self._get_timing(checksum, i) for i in range(4))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            3200, -1600, 400, -400, 400, -1200, 400, -400, 400, -1200, 400, -400, 400, -1200, 
            400, -400, 400, -1200, 400, -400, 400, -1200, 400, -400, 400, -1200, 400, -1200, 
            400, -400, 400, -1200, 400, -400, 400, -1200, 400, -1200, 400, -1200, 400, -1200, 
            400, -1200, 400, -1200, 400, -400, 400, -1200, 400, -400, 400, -400, 400, -400, 
            400, -1200, 400, -1200, 400, -1200, 400, -400, 400, -1200, 400, -1200, 400, -400, 
            400, -1200, 400, -400, 400, -400, 400, -400, 400, -400, 400, -400, 400, -400, 
            400, -1200, 400, -400, 400, -1200, 400, -1200, 400, -1200, 400, -1200, 400, -400, 
            400, -19200, 
        ]]

        params = [dict(function=5, sub_device=184, device=11, extended_function=10)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=5, sub_device=184, device=11, extended_function=10)
        protocol_base.IrProtocolBase._test_encode(self, params)


SharpDVD = SharpDVD()
