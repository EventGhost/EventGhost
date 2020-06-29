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


TIMING = 444


class RC6M32(protocol_base.IrProtocolBase):
    """
    IR decoder for the RC6M32 protocol.
    """
    irp = '{36k,444,msb}<-1,1|1,-1>(6,-2,1:1,M:3,<-2,2|2,-2>(1-(T:1)),OEM1:8,OEM2:8,D:8,F:8,^107m)*'
    frequency = 36000
    bit_count = 37
    encoding = 'msb'

    _lead_in = [TIMING * 6, -TIMING * 2]
    _lead_out = [107000]
    _middle_timings = [{'start': 4, 'stop': 5, 'bursts': [[-TIMING * 2, TIMING * 2], [TIMING * 2, -TIMING * 2]]}]
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['M', 1, 3],
        ['T', 4, 4],
        ['OEM1', 5, 12],
        ['OEM2', 13, 20],
        ['D', 21, 28],
        ['F', 29, 36],
    ]
    # [OEM1:0..255,OEM2:0..255,D:0..255,F:0..255,M:0..7,T@:0..1=0]
    encode_parameters = [
        ['mode', 0, 7],
        ['device', 0, 255],
        ['function', 0, 255],
        ['toggle', 0, 1],
        ['oem1', 0, 255],
        ['oem2', 0, 255]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 1:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, mode, device, function, toggle, oem1, oem2):
        c0 = 1

        t_bursts = [[-TIMING * 2, TIMING * 2], [TIMING * 2, -TIMING * 2]]

        toggle = t_bursts[toggle]

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(mode, i) for i in range(3)),
            toggle,
            list(self._get_timing(oem1, i) for i in range(8)),
            list(self._get_timing(oem2, i) for i in range(8)),
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            2664, -888, 444, -444, 444, -444, 444, -888, 444, -888, 888, -444, 444, -444,
            444, -444, 444, -444, 888, -888, 444, -444, 888, -444, 444, -888, 444, -444, 444, -444,
            888, -888, 444, -444, 888, -888, 888, -888, 444, -444, 888, -888, 888, -444, 444, -888,
            444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 888, -70148,
        ]]

        params = [dict(function=1, toggle=0, device=75, oem2=137, oem1=9, mode=6)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=1, toggle=0, device=75, oem2=137, oem1=9, mode=6)
        protocol_base.IrProtocolBase._test_encode(self, params)


RC6M32 = RC6M32()
