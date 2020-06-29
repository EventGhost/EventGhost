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


TIMING = 182


class Digivision(protocol_base.IrProtocolBase):
    """
    IR decoder for the Digivision protocol.
    """
    irp = '{38.0k,182,lsb}<3,-3|3,-6>(20,-10,D:8,Dev2:8,Dev3:8,20,-10,F:8,~F:8,3,^108m,(20,-20,3,^108m)*)'
    frequency = 38400
    bit_count = 40
    encoding = 'lsb'

    _lead_in = [TIMING * 20, -TIMING * 10]
    _lead_out = [TIMING * 3, 108000]
    _middle_timings = [(TIMING * 20, -TIMING * 10)]
    _bursts = [[TIMING * 3, -TIMING * 3], [TIMING * 3, -TIMING * 6]]

    _repeat_lead_in = [TIMING * 20, -TIMING * 20]
    _repeat_lead_out = [TIMING * 3, 108000]
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['D2', 8, 15],
        ['D3', 16, 23],
        ['F', 24, 31],
        ['F_CHECKSUM', 32, 39]
    ]
    # [D:0..255,Dev2:0..255,Dev3:0..255,F:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['device2', 0, 255],
        ['device3', 0, 255],
        ['function', 0, 255]
    ]

    def _calc_checksum(self, function):
        f = self._invert_bits(function, 8)
        return f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        func_checksum = self._calc_checksum(code.function)

        if func_checksum != code.f_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, device_2, device_3, function):
        func_checksum = self._calc_checksum(function)

        encoded_dev = list(
            self._get_timing(device, i) for i in range(8)
        )
        encoded_dev2 = list(
            self._get_timing(device_2, i) for i in range(8)
        )
        encoded_dev3 = list(
            self._get_timing(device_3, i) for i in range(8)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )
        encoded_func_check = list(
            self._get_timing(func_checksum, i) for i in range(8)
        )

        packet = self._build_packet(
            encoded_dev,
            encoded_dev2,
            encoded_dev3,
            [self._middle_timings],
            encoded_func,
            encoded_func_check,
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3640, -1820, 546, -1092, 546, -1092, 546, -546, 546, -546, 546, -1092, 546, -546, 546, -1092,
            546, -1092, 546, -546, 546, -1092, 546, -1092, 546, -546, 546, -1092, 546, -546, 546, -1092,
            546, -546, 546, -1092, 546, -1092, 546, -1092, 546, -1092, 546, -546, 546, -546, 546, -1092,
            546, -546, 3640, -1820, 546, -1092, 546, -1092, 546, -1092, 546, -1092, 546, -546, 546, -546,
            546, -1092, 546, -1092, 546, -546, 546, -546, 546, -546, 546, -546, 546, -1092, 546, -1092,
            546, -546, 546, -546, 546, -40842
        ]]

        params = [dict(function=207, d3=79, d2=86, device=211)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=207, device3=79, device2=86, device=211)
        protocol_base.IrProtocolBase._test_encode(self, params)

Digivision = Digivision()
