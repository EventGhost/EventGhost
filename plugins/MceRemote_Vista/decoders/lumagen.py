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


TIMING = 416


class Lumagen(protocol_base.IrProtocolBase):
    """
    IR decoder for the Lumagen protocol.
    """
    irp = '{38.4k,416,msb}<1,-6|1,-12>(D:4,C:1,F:7,1,-26)*{C=(#F+1)&1}'
    frequency = 38400
    bit_count = 12
    encoding = 'msb'

    _lead_in = []
    _lead_out = [TIMING, -TIMING * 26]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 6], [TIMING, -TIMING * 12]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 8]
    _repeat_lead_out = [TIMING, 108000]
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 3],
        ['CHECKSUM', 4, 4],
        ['F', 5, 11],
    ]
    # [D:0..15,F:0..127]
    encode_parameters = [
        ['device', 0, 15],
        ['function', 0, 127],
    ]

    def _calc_checksum(self, function):
        return (self._count_one_bits(function) + 1) & 1

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
            list(self._get_timing(checksum, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(7))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            416, -4992, 416, -4992, 416, -2496, 416, -4992, 416, -4992, 416, -4992, 416, -2496, 416, -4992,
            416, -2496, 416, -2496, 416, -4992, 416, -4992, 416, -10816
        ]]

        params = [dict(device=13, function=83)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=13, function=83)
        protocol_base.IrProtocolBase._test_encode(self, params)


Lumagen = Lumagen()
