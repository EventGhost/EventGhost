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


TIMING = 535


class DishPlayer(protocol_base.IrProtocolBase):
    """
    IR decoder for the DishPlayer protocol.
    """
    irp = '{38.4k,535,msb}<1,-5|1,-3>(1,-11,(F:6,S:5,D:2,1,-11)+)'
    frequency = 38400
    bit_count = 13
    encoding = 'msb'

    _lead_in = [TIMING, -TIMING * 11]
    _lead_out = [TIMING, -TIMING * 11]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 5], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['F', 0, 5],
        ['S', 6, 10],
        ['D', 11, 12],
    ]
    # [F:0..63,S:0..31,D:0..3]
    encode_parameters = [
        ['device', 0, 3],
        ['sub_device', 0, 31],
        ['function', 0, 63],
        ['extended_function', 0, 255]
    ]

    def decode(self, data, frequency=0):
        if self._last_code is not None:
            self._lead_in = []
        else:
            self._lead_in = [TIMING, -TIMING * 11]

        try:
            code = protocol_base.IrProtocolBase.decode(data, frequency)
        except DecodeError:
            self._lead_in = [TIMING, -TIMING * 11]
            self._last_code = None
            raise

        if self._last_code is None:
            self._last_code = code

        elif code != self._last_code:
            self._last_code = None
            self._lead_in = [TIMING, -TIMING * 11]
            raise DecodeError('Repeat code does not match')

        return self._last_code

    def encode(self, device, sub_device, function):
        packet = self._build_packet(
            list(self._get_timing(function, i) for i in range(6)),
            list(self._get_timing(sub_device, i) for i in range(5)),
            list(self._get_timing(device, i) for i in range(2)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [
            [
                +535, -5885, +535, -2675, +535, -2675, +535, -2675, +535, -1605, +535, -2675, +535, -1605, +535, -2675,
                +535, -2675, +535, -2675, +535, -2675, +535, -1605, +535, -2675, +535, -2675, +535, -5885
            ],
            [
                +535, -2675, +535, -2675, +535, -2675, +535, -1605, +535, -2675, +535, -1605, +535, -2675, +535, -2675,
                +535, -2675, +535, -2675, +535, -1605, +535, -2675, +535, -2675, +535, -5885
            ]

        ]

        params = [dict(device=0, function=5, sub_device=1), dict(device=0, function=5, sub_device=1)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=0, function=5, sub_device=1)
        protocol_base.IrProtocolBase._test_encode(self, params)


DishPlayer = DishPlayer()
