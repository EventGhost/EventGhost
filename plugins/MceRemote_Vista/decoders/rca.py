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


TIMING = 460


class RCA(protocol_base.IrProtocolBase):
    """
    IR decoder for the RCA protocol.
    """
    irp = '{58k,460,msb}<1,-2|1,-4>(8,-8,D:4,F:8,~D:4,~F:8,1,-16)*'
    frequency = 58000
    bit_count = 24
    encoding = 'msb'

    _lead_in = [TIMING * 8, -TIMING * 8]
    _lead_out = [TIMING, -TIMING * 16]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 2], [TIMING, -TIMING * 4]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []
    # D:4,F:8,~D:4,~F:8
    _parameters = [
        ['D', 0, 3],
        ['F', 4, 11],
        ['D_CHECKSUM', 12, 15],
        ['F_CHECKSUM', 16, 23]
    ]
    # [D:0..15,F:0..255]
    encode_parameters = [
        ['device', 0, 15],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, device, function):
        d = self._invert_bits(device, 4)
        f = self._invert_bits(function, 8)
        return d, f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        d_checksum, f_checksum = self._calc_checksum(code.device, code.function)

        if f_checksum != code.f_checksum or d_checksum != code.d_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        d_checksum, f_checksum = self._calc_checksum(
            device,
            function,
        )

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(d_checksum, i) for i in range(4)),
            list(self._get_timing(f_checksum, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            3680, -3680, 460, -1840, 460, -920, 460, -1840, 460, -1840, 460, -920, 460, -1840, 
            460, -1840, 460, -1840, 460, -1840, 460, -920, 460, -1840, 460, -1840, 460, -920, 
            460, -1840, 460, -920, 460, -920, 460, -1840, 460, -920, 460, -920, 460, -920, 
            460, -920, 460, -1840, 460, -920, 460, -920, 460, -7360, 
        ]]

        params = [dict(device=11, function=123)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=11, function=123)
        protocol_base.IrProtocolBase._test_encode(self, params)


RCA = RCA()
