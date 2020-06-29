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


TIMING = 398


class Elan(protocol_base.IrProtocolBase):
    """
    IR decoder for the 48NEC protocol.
    """
    irp = '{0k,398,msb}<1,-1|1,-2>(3,-2,D:8,~D:8,2,-2,F:8,~F:8,1,^50m)*'
    frequency = 0
    bit_count = 32
    encoding = 'msb'

    _lead_in = [TIMING * 3, -TIMING * 2]
    _lead_out = [TIMING, 50000]
    _middle_timings = [(TIMING * 2, -TIMING * 2)]
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 2]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['D_CHECKSUM', 8, 15],
        ['F', 16, 23],
        ['F_CHECKSUM', 24, 31]
    ]
    # [D:0..255,F:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, device, function):
        d = self._invert_bits(device, 8)
        f = self._invert_bits(function, 8)
        return d, f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        dev_checksum, func_checksum = self._calc_checksum(code.device, code.function)

        if dev_checksum != code.d_checksum or func_checksum != code.f_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        dev_checksum, func_checksum = self._calc_checksum(
            device,
            function
        )
        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(dev_checksum, i) for i in range(8)),
            self._middle_timings[0],
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(func_checksum, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            1194, -796, 398, -398, 398, -796, 398, -796, 398, -796, 398, -398, 398, -796, 398, -398, 398, -796,
            398, -796, 398, -398, 398, -398, 398, -398, 398, -796, 398, -398, 398, -796, 398, -398, 796, -796,
            398, -398, 398, -796, 398, -796, 398, -398, 398, -796, 398, -796,  398, -796, 398, -398, 398, -796,
            398, -398, 398, -398, 398, -796, 398, -398, 398, -398, 398, -398, 398, -796, 398, -14180
        ]]

        params = [dict(device=117, function=110)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=117, function=110)
        protocol_base.IrProtocolBase._test_encode(self, params)


Elan = Elan()
