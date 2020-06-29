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

TIMING = 550


class Aiwa(protocol_base.IrProtocolBase):
    """
    IR decoder for the Aiwa protocol.
    """
    irp = '{38.123k,550,lsb}<1,-1|1,-3>(16,-8,D:8,S:5,~D:8,~S:5,F:8,~F:8,1,-42,(16,-8,1,-165)*)'
    frequency = 38123
    bit_count = 42
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, -TIMING * 42]
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 8]
    _repeat_lead_out = [TIMING, -TIMING * 165]
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 12],
        ['D_CHECKSUM', 13, 20],
        ['S_CHECKSUM', 21, 25],
        ['F', 26, 33],
        ['F_CHECKSUM', 34, 41],
    ]
    # [D:0..255,S:0..31,F:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['sub_device', 0, 31],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, device, sub_device, function):
        d = self._invert_bits(device, 8)
        s = self._invert_bits(sub_device, 5)
        f = self._invert_bits(function, 8)

        return d, s, f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        device_checksum, sub_checksum, func_checksum = (
            self._calc_checksum(code.device, code.sub_device, code.function)
        )

        if (
            device_checksum != code.d_checksum or
            sub_checksum != code.s_checksum or
            func_checksum != code.f_checksum
        ):
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function):
        dev_checksum, sub_checksum, func_checksum = (
            self._calc_checksum(device, sub_device, function)
        )

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(5)),
            list(self._get_timing(dev_checksum, i) for i in range(8)),
            list(self._get_timing(sub_checksum, i) for i in range(5)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(func_checksum, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [
            [
                +8800, -4400, +550, -550, +550, -1650, +550, -550, +550, -550, +550, -550, +550, -1650, +550, -550,
                +550, -550, +550, -1650, +550, -550, +550, -550, +550, -550, +550, -1650, +550, -1650, +550, -550,
                +550, -1650, +550, -1650, +550, -1650, +550, -550, +550, -1650, +550, -1650, +550, -550, +550, -1650,
                +550, -1650, +550, -1650, +550, -550, +550, -550, +550, -1650, +550, -1650, +550, -1650, +550, -550,
                +550, -550, +550, -550, +550, -550, +550, -1650, +550, -550, +550, -550, +550, -550, +550, -1650,
                +550, -1650, +550, -1650, +550, -1650, +550, -23100
            ],
            [
                +8800, -4400, +550, -90750
            ]
        ]

        params = [dict(device=34, function=14, sub_device=17), dict(device=34, function=14, sub_device=17)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=34, function=14, sub_device=17)
        protocol_base.IrProtocolBase._test_encode(self, params)


Aiwa = Aiwa()
