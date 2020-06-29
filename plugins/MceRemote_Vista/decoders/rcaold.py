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
from . import DecodeError, RepeatLeadOut


TIMING = 460


class RCAOld(protocol_base.IrProtocolBase):
    """
    IR decoder for the RCAOld protocol.
    """
    irp = '{58k,460,msb}<1,-2|1,-4>([40][8],-8,D:4,F:8,~D:4,~F:8,2,-16)'
    frequency = 58000
    bit_count = 24
    encoding = 'msb'

    _lead_in = [TIMING * 40, -TIMING * 8]
    _lead_out = [TIMING * 2, -TIMING * 16]
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
        if self._lead_in[0] == TIMING * 8:
            self._lead_in[0] = TIMING * 40
        else:
            self._lead_in[0] = TIMING * 8

        d_checksum, f_checksum = self._calc_checksum(code.device, code.function)

        if f_checksum != code.f_checksum or d_checksum != code.d_checksum:
            self._lead_in[0] = TIMING * 40
            raise DecodeError('Checksum failed')

        if self._lead_in[0] == TIMING * 40:
            raise RepeatLeadOut

        return code

    def encode(self, device, function):
        d_checksum, f_checksum = self._calc_checksum(
            device,
            function,
        )

        lead_in = self._lead_in[0]

        self._lead_in[0] = TIMING * 40

        packet1 = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(d_checksum, i) for i in range(4)),
            list(self._get_timing(f_checksum, i) for i in range(8))
        )

        self._lead_in[0] = TIMING * 8

        packet2 = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(d_checksum, i) for i in range(4)),
            list(self._get_timing(f_checksum, i) for i in range(8))
        )

        self._lead_in[0] = lead_in

        return [packet1, packet2]

    def _test_decode(self):
        rlc =[
            [
                18400, -3680, 460, -1840, 460, -920, 460, -1840, 460, -1840, 460, -1840, 460, -920, 460, -1840,
                460, -920, 460, -1840, 460, -920, 460, -920, 460, -1840, 460, -920, 460, -1840, 460, -920,
                460, -920, 460, -920, 460, -1840, 460, -920, 460, -1840, 460, -920, 460, -1840, 460, -1840,
                460, -920, 920, -7360
            ],
            [
                3680, -3680, 460, -1840, 460, -920, 460, -1840, 460, -1840, 460, -1840, 460, -920, 460, -1840,
                460, -920, 460, -1840, 460, -920, 460, -920, 460, -1840, 460, -920, 460, -1840, 460, -920,
                460, -920, 460, -920, 460, -1840, 460, -920, 460, -1840, 460, -920, 460, -1840, 460, -1840,
                460, -920, 920, -7360
            ]
        ]

        params = [dict(device=11, function=169), None]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=11, function=169)
        protocol_base.IrProtocolBase._test_encode(self, params)


RCAOld = RCAOld()
