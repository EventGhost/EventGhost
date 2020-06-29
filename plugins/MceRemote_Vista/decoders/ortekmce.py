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


TIMING = 480


class OrtekMCE(protocol_base.IrProtocolBase):
    """
    IR decoder for the OrtekMCE protocol.
    """
    irp = '{38.6k,480,lsb}<1,-1|-1,1>([P=0][P=1][P=2],4,-1,D:5,P:2,F:6,C:4,-48m)+{C=3+#D+#P+#F}'
    frequency = 38600
    bit_count = 17
    encoding = 'lsb'

    _lead_in = [TIMING * 4, -TIMING]
    _lead_out = [-48000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [-TIMING, TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 4],
        ['P', 5, 6],
        ['F', 7, 12],
        ['CHECKSUM', 13, 16]
    ]
    # [D:0..31,F:0..63]
    encode_parameters = [
        ['device', 0, 31],
        ['function', 0, 63],
    ]

    def _calc_checksum(self, device, function, p):
        d = self._count_one_bits(device)
        f = self._count_one_bits(function)
        p = self._count_one_bits(p)

        return self._get_bits(3 + d + f + p, 0, 3)

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.device, code.function, code.p)

        if checksum != code.checksum or code.p not in (0, 1, 2):
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        codes = []
        
        for p in range(3):
            
            checksum = self._calc_checksum(
                device,
                function,
                p
            )
            packet = self._build_packet(
                list(self._get_timing(device, i) for i in range(5)),
                list(self._get_timing(p, i) for i in range(2)),
                list(self._get_timing(function, i) for i in range(6)),
                list(self._get_timing(checksum, i) for i in range(4))
            )
            codes += [packet]

        return codes

    def _test_decode(self):
        rlc = [
            [
                1920, -480, 480, -960, 480, -480, 480, -480, 480, -480, 960, -480, 480, -480, 480, -960, 480, -480, 480, -480,
                480, -480, 480, -480, 960, -480, 480, -960, 480, -480, 480, -48000
            ],
            [
                1920, -480, 480, -960, 480, -480, 480, -480, 480, -480, 480, -480, 960, -480, 480, -960, 480, -480, 480, -480,
                480, -480, 480, -480, 480, -480, 960, -960, 480, -480, 480, -48000
            ],
            [
                1920, -480, 480, -960, 480, -480, 480, -480, 480, -480, 960, -960, 960, -960, 480, -480, 480, -480, 480, -480,
                480, -480, 480, -480, 960, -960, 480, -480, 480, -48000
            ]
        ]

        params = [
            dict(device=30, function=62, p=0),
            dict(device=30, function=62, p=1),
            dict(device=30, function=62, p=2)
        ]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=30, function=62)
        protocol_base.IrProtocolBase._test_encode(self, params)


OrtekMCE = OrtekMCE()
