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

TIMING = 477


class Akord(protocol_base.IrProtocolBase):
    """
    IR decoder for the Akord protocol.
    """
    irp = '{37.0k,477,msb}<1,-1|1,-2>(18,-8,D:8,S:8,F:8,~F:8,1,-40m,(18,-5,1,-78m)*)'
    frequency = 37000
    bit_count = 32
    encoding = 'msb'

    _lead_in = [TIMING * 18, -TIMING * 8]
    _lead_out = [TIMING, -40000]
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 2]]

    _repeat_lead_in = [TIMING * 18, -TIMING * 5]
    _repeat_lead_out = [TIMING, -TIMING * 78]
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['F', 16, 23],
        ['F_CHECKSUM', 24, 31]
    ]
    # [D:0..255,S:0..255,F:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['sub_device', 0, 255],
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

    def encode(self, device, sub_device, function):
        func_checksum = self._calc_checksum(function)

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(func_checksum, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            8586, -3816, 477, -477, 477, -954, 477, -954, 477, -954, 477, -954, 477, -954, 477, -477, 477, -954,
            477, -477, 477, -954, 477, -954, 477, -477, 477, -954, 477, -477, 477, -954, 477, -477, 477, -477,
            477, -954, 477, -477, 477, -477, 477, -954, 477, -954, 477, -477, 477, -954, 477, -954, 477, -477,
            477, -954, 477, -954, 477, -477, 477, -477, 477, -954, 477, -477, 477, -40000
        ]]

        params = [dict(device=125, function=77, sub_device=106)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=125, function=77, sub_device=106)
        protocol_base.IrProtocolBase._test_encode(self, params)


Akord = Akord()
