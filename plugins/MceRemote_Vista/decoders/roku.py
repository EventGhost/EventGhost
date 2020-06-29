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


TIMING = 564


class Roku(protocol_base.IrProtocolBase):
    """
    IR decoder for the Roku protocol.
    """
    irp = '{38.0k,564,lsb}<1,-1|1,-3>(16,-8,D:8,S:8,F:7,0:1,~F:7,1:1,1,^108m,(16,-8,D:8,S:8,F:7,1:1,~F:7,0:1,1,^108m)*)'
    frequency = 38000
    bit_count = 32
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 108000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['F', 16, 22],
        ['C0', 23, 23],
        ['F_CHECKSUM', 24, 30],
        ['C1', 31, 31]
    ]
    # [D:0..255,S:0..255=255-D,F:0..127]
    encode_parameters = [
        ['device', 0, 255],
        ['sub_device', 0, 255],
        ['function', 0, 127],
    ]

    def _calc_checksum(self, function):
        f = self._invert_bits(function, 7)
        return f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        func_checksum = self._calc_checksum(code.function)

        if func_checksum != code.f_checksum or code.c0 != 0 or code.c1 != 1:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function):
        c0 = 0
        c1 = 1
        func_checksum = self._calc_checksum(function)

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(7)),
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(func_checksum, i) for i in range(7)),
            list(self._get_timing(c1, i) for i in range(1)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            9024, -4512, 564, -1692, 564, -1692, 564, -564, 564, -564, 564, -1692, 564, -564, 
            564, -564, 564, -564, 564, -1692, 564, -564, 564, -564, 564, -564, 564, -1692, 
            564, -564, 564, -564, 564, -564, 564, -1692, 564, -564, 564, -564, 564, -1692, 
            564, -564, 564, -1692, 564, -1692, 564, -564, 564, -564, 564, -1692, 564, -1692, 
            564, -564, 564, -1692, 564, -564, 564, -564, 564, -1692, 564, -43140, 
        ]]

        params = [dict(device=19, function=105, sub_device=17)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=19, function=105, sub_device=17)
        protocol_base.IrProtocolBase._test_encode(self, params)


Roku = Roku()
