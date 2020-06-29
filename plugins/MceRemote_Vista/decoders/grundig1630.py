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


TIMING = 578


# TODO: Finish
class Grundig1630(protocol_base.IrProtocolBase):
    """
    IR decoder for the Grundig1630 protocol.
    """
    irp = '{30.3k,578,msb}<-4,2|-3,1,-1,1|-2,1,-2,1|-1,1,-3,1>(806u,-2960u,1346u,T:1,F:8,D:7,-100)*[D:0..127,F:0..255,T:0..1]'
    frequency = 53700
    bit_count = 48
    encoding = 'msb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 108000]
    _middle_timings = []
    _bursts = [[-TIMING * 4, TIMING * 2], [-TIMING * 3, TIMING], [-TIMING, TIMING], [-TIMING * 2, TIMING], [-TIMING * 2, ]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 8]
    _repeat_lead_out = [TIMING, 108000]
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['F', 16, 23],
        ['F_CHECKSUM', 24, 31],
        ['E', 32, 39],
        ['E_CHECKSUM', 40, 47]
    ]
    # [D:0..255,S:0..255=255-D,F:0..255,E:0..255]
    encode_parameters = [
        # ['device', 0, 255],
        # ['sub_device', 0, 255],
        # ['function', 0, 255],
        # ['extended_function', 0, 255]
    ]

    def _calc_checksum(self, function, e):
        f = self._invert_bits(function, 8)
        e = self._invert_bits(e, 8)
        return f, e

    def decode(self, data, frequency=0):
        raise DecodeError
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        func_checksum, e_checksum = self._calc_checksum(code.function, code.e)

        if func_checksum != code.f_checksum or e_checksum != code.e_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function, extended_function):
        func_checksum, ex_func_checksum = self._calc_checksum(
            function,
            extended_function
        )

        list(self._get_timing(device, i) for i in range(8)),
        list(self._get_timing(sub_device, i) for i in range(8)),
        list(self._get_timing(function, i) for i in range(8)),
        list(self._get_timing(e, i) for i in range(8)),
        list(self._get_timing(func_checksum, i) for i in range(8)),
        list(self._get_timing(ex_func_checksum, i) for i in range(8)),

        packet = self._build_packet(
            encoded_dev,
            encoded_sub,
            encoded_func,
            encoded_func_check,
            encoded_e,
            encoded_ex_func_check
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        return
        rlc = [
            806, -2960, 1346, -1156, 578, -1156, 578, -1734, 578, -578, 578, -2312, 1156, -2312, 1156, -2312,
            1156, -1734, 578, -578, 578, -1156, 578, -1156, 578, -1156, 578, -1156, 578, -57800
        ]

        params = dict(device=26, function=32, toggle=1)
        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        return
        params = dict(device=26, function=32, toggle=1)
        protocol_base.IrProtocolBase._test_encode(self, params)


Grundig1630 = Grundig1630()
