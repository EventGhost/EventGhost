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

TIMING = 413


class Fujitsu128(protocol_base.IrProtocolBase):
    """
    IR decoder for the Fujitsu128 protocol.
    """
    irp = '{38.4k,413,lsb}<1,-1|1,-3>(8,-4,A0:8,A1:8,A2:8,A3:8,A4:8,A5:8,A6:8,A7:8,A8:8,A9:8,A10:8,A11:8,A12:8,A13:8,A14:8,A15:8,1,-104.3m)*'
    frequency = 38400
    bit_count = 128
    encoding = 'lsb'

    _lead_in = [TIMING * 8, -TIMING * 4]
    _lead_out = [TIMING, -104300]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []
    _parameters = [
        ['A0', 0, 7],
        ['A1', 8, 15],
        ['A2', 16, 23],
        ['A3', 24, 31],
        ['A4', 32, 39],
        ['A5', 40, 47],
        ['A6', 48, 55],
        ['A7', 56, 63],
        ['A8', 64, 71],
        ['A9', 72, 79],
        ['A10', 80, 87],
        ['A11', 88, 95],
        ['A12', 96, 103],
        ['A13', 104, 111],
        ['A14', 112, 119],
        ['A15', 120, 127],
    ]
    # [
    # A0:0..255,
    # A1:0..255,
    # A2:0..255,
    # A3:0..255,
    # A4:0..255,
    # A5:0..255,
    # A6:0..255,
    # A7:0..255,
    # A8:0..255,
    # A9:0..255,
    # A10:0..255,
    # A11:0..255,
    # A12:0..255,
    # A13:0..255,
    # A14:0..255,
    # A15:0..255
    # ]
    encode_parameters = [
        ['A0', 0, 255],
        ['a1', 0, 255],
        ['a2', 0, 255],
        ['a3', 0, 255],
        ['a4', 0, 255],
        ['a5', 0, 255],
        ['a6', 0, 255],
        ['a7', 0, 255],
        ['a8', 0, 255],
        ['a9', 0, 255],
        ['a10', 0, 255],
        ['a11', 0, 255],
        ['a12', 0, 255],
        ['a13', 0, 255],
        ['a14', 0, 255],
        ['a15', 0, 255],
    ]

    def encode(
        self,
        a0,
        a1,
        a2,
        a3,
        a4,
        a5,
        a6,
        a7,
        a8,
        a9,
        a10,
        a11,
        a12,
        a13,
        a14,
        a15
    ):
        items = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a14, a15]

        for i, item in enumerate(items):
            encoded = list(
                self._get_timing(item, i) for i in range(8)
            )

            items[i] = encoded

        packet = self._build_packet(*items)

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3304, -1652, 413, -1239, 413, -1239, 413, -413, 413, -1239, 413, -413, 413, -413, 413, -413,
            413, -413, 413, -1239, 413, -1239, 413, -413, 413, -413, 413, -413, 413, -1239, 413, -413,
            413, -1239, 413, -413, 413, -413, 413, -1239, 413, -1239, 413, -1239, 413, -1239, 413, -413,
            413, -1239, 413, -413, 413, -1239, 413, -1239, 413, -1239, 413, -413, 413, -413, 413, -413,
            413, -1239, 413, -413, 413, -413, 413, -1239, 413, -1239, 413, -1239, 413, -413, 413, -1239,
            413, -413, 413, -413, 413, -1239, 413, -413, 413, -413, 413, -413, 413, -1239, 413, -1239,
            413, -413, 413, -1239, 413, -413, 413, -413, 413, -1239, 413, -413, 413, -413, 413, -1239,
            413, -413, 413, -1239, 413, -413, 413, -413, 413, -413, 413, -1239, 413, -1239, 413, -1239,
            413, -413, 413, -1239, 413, -413, 413, -1239, 413, -1239, 413, -1239, 413, -1239, 413, -413,
            413, -413, 413, -413, 413, -413, 413, -1239, 413, -413, 413, -1239, 413, -1239, 413, -413,
            413, -413, 413, -1239, 413, -413, 413, -413, 413, -1239, 413, -413, 413, -1239, 413, -413,
            413, -1239, 413, -413, 413, -413, 413, -1239, 413, -413, 413, -413, 413, -413, 413, -1239,
            413, -1239, 413, -1239, 413, -413, 413, -1239, 413, -413, 413, -1239, 413, -1239, 413, -413,
            413, -413, 413, -413, 413, -413, 413, -413, 413, -413, 413, -413, 413, -1239, 413, -413,
            413, -1239, 413, -413, 413, -1239, 413, -413, 413, -1239, 413, -413, 413, -1239, 413, -413,
            413, -1239, 413, -1239, 413, -413, 413, -1239, 413, -1239, 413, -1239, 413, -1239, 413, -1239,
            413, -1239, 413, -104300
        ]]
        params = [dict(
            a0=11, a1=163, a2=188, a3=142, a4=92, a5=98, a6=73, a7=113, a8=61,
            a9=52, a10=169, a11=196, a12=53, a13=160, a14=170, a15=253
        )]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(
            a0=11, a1=163, a2=188, a3=142, a4=92, a5=98, a6=73, a7=113, a8=61,
            a9=52, a10=169, a11=196, a12=53, a13=160, a14=170, a15=253
        )
        protocol_base.IrProtocolBase._test_encode(self, params)


Fujitsu128 = Fujitsu128()
