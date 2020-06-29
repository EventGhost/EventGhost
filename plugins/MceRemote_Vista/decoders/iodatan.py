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


class IODATAn(protocol_base.IrProtocolBase):
    """
    IR decoder for the IODATAn protocol.
    """
    irp = '{38k,550,lsb}<1,-1|1,-3>(16,-8,x:7,D:7,S:7,y:7,F:8,C:4,1,^108m)*'
    frequency = 38000
    bit_count = 40
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 108000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['X', 0, 6],
        ['D', 7, 13],
        ['S', 14, 20],
        ['Y', 21, 27],
        ['F', 28, 35],
        ['C', 36, 39],
    ]
    # [D:0..127,S:0..127,F:0..255,C:0..15=0,x:0..127=0,y:0..127=0]
    encode_parameters = [
        ['device', 0, 127],
        ['sub_device', 0, 127],
        ['function', 0, 255],
        ['c', 0, 15],
        ['x', 0, 127],
        ['y', 0, 127]
    ]

    def encode(self, device, sub_device, function, c, x, y):
        encoded_dev = list(
            self._get_timing(device, i) for i in range(7)
        )
        encoded_sub = list(
            self._get_timing(sub_device, i) for i in range(7)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )
        encoded_c = list(
            self._get_timing(c, i) for i in range(4)
        )
        encoded_x = list(
            self._get_timing(x, i) for i in range(7)
        )
        encoded_y = list(
            self._get_timing(y, i) for i in range(7)
        )

        packet = self._build_packet(
            encoded_x,
            encoded_dev,
            encoded_sub,
            encoded_y,
            encoded_func,
            encoded_c,
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            8800, -4400, 550, -550, 550, -1650, 550, -550, 550, -550, 550, -1650, 550, -550, 550, -550, 550, -550,
            550, -1650, 550, -550, 550, -550, 550, -550, 550, -550, 550, -550, 550, -1650, 550, -550, 550, -550,
            550, -1650, 550, -1650, 550, -550, 550, -550, 550, -550, 550, -550, 550, -550, 550, -1650, 550, -1650,
            550, -1650, 550, -1650, 550, -550, 550, -1650, 550, -1650, 550, -550, 550, -1650, 550, -550, 550, -550,
            550, -550, 550, -1650, 550, -1650, 550, -550, 550, -550, 550, -33750
        ]]

        params = [dict(device=2, c=3, function=22, sub_device=25, x=18, y=120)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=2, c=3, function=22, sub_device=25, x=18, y=120)
        protocol_base.IrProtocolBase._test_encode(self, params)


IODATAn = IODATAn()
