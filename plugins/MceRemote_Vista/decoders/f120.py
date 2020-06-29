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

TIMING = 422


class F120(protocol_base.IrProtocolBase):
    """
    IR decoder for the F120 protocol.
    """
    irp = '{37.9k,422,lsb}<1,-3|3,-1>(D:3,H:1,F:8,-34,D:3,H:1,F:8){H=0}'
    frequency = 37900
    bit_count = 24
    encoding = 'lsb'

    _lead_in = []
    _lead_out = []
    _middle_timings = [-TIMING * 34]
    _bursts = [[TIMING, -TIMING * 3], [TIMING * 3, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 2],
        ['H', 3, 3],
        ['F', 4, 11],
        ['D1', 12, 14],
        ['H1', 15, 15],
        ['F1', 16, 23]
    ]
    # [D:0..7,F:0..255]
    encode_parameters = [
        ['device', 0, 7],
        ['function', 0, 255]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if (
            code.device != code.d1 or
            code.h != 0 != code.h1 or
            code.function != code.f1
        ):
            raise DecodeError('Invalid checksum')

        return code

    def encode(self, device, function):
        h = 0

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(3)),
            list(self._get_timing(h, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(8)),
            self._middle_timings,
            list(self._get_timing(device, i) for i in range(3)),
            list(self._get_timing(h, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [
            [
                +1266, -422, +422, -1266, +1266, -422, +422, -1266, +422, -1266, +422, -1266, +422, -1266, +1266, -422,
                +1266, -422, +1266, -422, +422, -1266, +422, -15614, +1266, -422, +422, -1266, +1266, -422, +422, -1266,
                +422, -1266, +422, -1266, +422, -1266, +1266, -422, +1266, -422, +1266, -422, +422, -1266, +422, -1266
            ]
        ]

        params = [dict(device=5, function=56)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=5, function=56)
        protocol_base.IrProtocolBase._test_encode(self, params)


F120 = F120()
