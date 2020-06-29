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


TIMING = 500


class Bose(protocol_base.IrProtocolBase):
    """
    IR decoder for the Bose protocol.
    """
    irp = '{38.0k,500,msb}<1,-1|1,-3>(2,-3,F:8,~F:8,1,-50m)*'
    frequency = 38000
    bit_count = 16
    encoding = 'msb'

    _lead_in = [TIMING * 2, -TIMING * 3]
    _lead_out = [TIMING, -50000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['F', 0, 7],
        ['F_CHECKSUM', 8, 15],
    ]
    # [F:0..255]
    encode_parameters = [
        ['function', 0, 255],
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

    def encode(self, function):
        func_checksum = self._calc_checksum(function)
        packet = self._build_packet(
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(func_checksum, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            1000, -1500, 500, -500, 500, -1500, 500, -1500, 500, -1500, 500, -500, 500, -1500,
            500, -1500, 500, -500, 500, -1500, 500, -500, 500, -500, 500, -500, 500, -1500,
            500, -500, 500, -500, 500, -1500, 500, -50000,
        ]]

        params = [dict(function=118)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=118)
        protocol_base.IrProtocolBase._test_encode(self, params)


Bose = Bose()
