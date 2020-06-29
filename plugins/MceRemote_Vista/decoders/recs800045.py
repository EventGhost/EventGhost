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


TIMING = 158


class RECS800045(protocol_base.IrProtocolBase):
    """
    IR decoder for the RECS800045 protocol.
    """
    irp = '{38k,158,msb}<1,-31|1,-47>(1:1,T:1,D:3,F:6,1,-45m)*'
    frequency = 38000
    bit_count = 11
    encoding = 'msb'

    _lead_in = []
    _lead_out = [TIMING, -45000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 31], [TIMING, -TIMING * 47]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['T', 1, 1],
        ['D', 2, 4],
        ['F', 5, 10],
    ]
    # [D:0..7,F:0..63,T@:0..1=0]
    encode_parameters = [
        ['device', 0, 7],
        ['function', 0, 63],
        ['toggle', 0, 1]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 1:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function, toggle):
        c0 = 1

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(3)),
            list(self._get_timing(function, i) for i in range(6)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            158, -7426, 158, -4898, 158, -4898, 158, -7426, 158, -7426, 158, -7426, 158, -4898, 
            158, -7426, 158, -4898, 158, -4898, 158, -7426, 158, -45000, 
        ]]

        params = [dict(function=41, toggle=0, device=3)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=41, toggle=0, device=3)
        protocol_base.IrProtocolBase._test_encode(self, params)


RECS800045 = RECS800045()
