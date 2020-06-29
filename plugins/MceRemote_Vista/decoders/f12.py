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


class F12(protocol_base.IrProtocolBase):
    """
    IR decoder for the F12 protocol.
    """
    irp = '{37.9k,422,lsb}<1,-3|3,-1>((D:3,S:1,F:8,-80)2)*'
    frequency = 37900
    bit_count = 24
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [-TIMING * 80]
    _middle_timings = [-TIMING * 80]
    _bursts = [[TIMING, -TIMING * 3], [TIMING * 3, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 2],
        ['S', 3, 3],
        ['F', 4, 11],
        ['D1', 12, 14],
        ['S1', 15, 15],
        ['F1', 16, 23]
    ]
    # [D:0..7,S:0..1,F:0..255]
    encode_parameters = [
        ['device', 0, 7],
        ['sub_device', 0, 1],
        ['function', 0, 255],
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.device != code.d1  or code.sub_device != code.s1 or code.function != code.f1:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function):

        encoded_dev = list(
            self._get_timing(device, i) for i in range(3)
        )
        encoded_sub = list(
            self._get_timing(sub_device, i) for i in range(1)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )

        packet = self._build_packet(
            encoded_dev,
            encoded_sub,
            encoded_func
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            1266, -422, 422, -1266, 1266, -422, 1266, -422, 422, -1266, 422, -1266, 1266, -422, 422, -1266,
            422, -1266, 1266, -422, 1266, -422, 1266, -34182, 1266, -422, 422, -1266, 1266, -422, 1266, -422,
            422, -1266, 422, -1266, 1266, -422, 422, -1266, 422, -1266, 1266, -422, 1266, -422, 1266, -34182
        ]]

        params = [dict(device=5, function=228, sub_device=1)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=5, function=228, sub_device=1)
        protocol_base.IrProtocolBase._test_encode(self, params)


F12 = F12()
