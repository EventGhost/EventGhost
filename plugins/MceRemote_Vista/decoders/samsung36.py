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


TIMING = 560


class Samsung36(protocol_base.IrProtocolBase):
    """
    IR decoder for the Samsung36 protocol.
    """
    irp = '{37.9k,560,lsb}<1,-1|1,-3>(4500u,-4500u,D:8,S:8,1,-9,E:4,F:8,~F:8,1,^108m)*'
    frequency = 37900
    bit_count = 36
    encoding = 'lsb'

    _lead_in = [4500, -4500]
    _lead_out = [TIMING, 108000]
    _middle_timings = [(TIMING, -TIMING * 9)]
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []
    # D:8,S:8,1,-9,E:4,F:8,~F:8
    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['E', 16, 19],
        ['F', 20, 27],
        ['CHECKSUM', 28, 35],
    ]
    # [D:0..255,S:0..255,F:0..255,E:0..15]
    encode_parameters = [
        ['device', 0, 255],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['extended_function', 0, 15]
    ]

    def _calc_checksum(self, function):
        f = self._invert_bits(function, 8)
        return f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.function)

        if checksum != code.checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function, extended_function):
        checksum = self._calc_checksum(function)

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            self._middle_timings,
            list(self._get_timing(extended_function, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(checksum, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            4500, -4500, 560, -560, 560, -560, 560, -1680, 560, -560, 560, -1680, 560, -560, 
            560, -1680, 560, -560, 560, -560, 560, -560, 560, -1680, 560, -560, 560, -560, 
            560, -560, 560, -1680, 560, -1680, 560, -5040, 560, -560, 560, -560, 560, -560, 
            560, -560, 560, -1680, 560, -560, 560, -560, 560, -1680, 560, -560, 560, -1680, 
            560, -560, 560, -1680, 560, -560, 560, -1680, 560, -1680, 560, -560, 560, -1680, 
            560, -560, 560, -1680, 560, -560, 560, -36840, 
        ]]

        params = [dict(function=169, sub_device=196, device=84, extended_function=0)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=169, sub_device=196, device=84, extended_function=0)
        protocol_base.IrProtocolBase._test_encode(self, params)


Samsung36 = Samsung36()
