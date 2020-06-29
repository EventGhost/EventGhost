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


TIMING = 500


class Thomson(protocol_base.IrProtocolBase):
    """
    IR decoder for the Thomson protocol.
    """
    irp = '{33k,500,lsb}<1,-4|1,-9>(D:4,(1-T):1,D:1:4,F:6,1,^80m)*'
    frequency = 33000
    bit_count = 12
    encoding = 'lsb'

    _lead_in = []
    _lead_out = [TIMING, 80000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 4], [TIMING, -TIMING * 9]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    # D:4,(1-T):1,D:1:4,F:6
    _parameters = [
        ['D', 0, 3],
        ['T', 4, 4],
        ['D1', 5, 5],
        ['F', 6, 11],
    ]
    # [D:0..31,F:0..63,T@:0..1=0]
    encode_parameters = [
        ['device', 0, 31],
        ['function', 0, 63],
        ['toggle', 0, 1]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        params = dict(
            D=self._set_bit(code.device, 4, self._get_bit(code.d1, 0)),
            F=code.function,
            CHECKSUM=code.checksum,
            T=code.toggle
        )

        return protocol_base.IRCode(self, code.original_rlc, code.normalized_rlc, params)

    def encode(self, device, function, toggle):
        d1 = self._get_bit(device, 4)

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(d1, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(6))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            500, -2000, 500, -2000, 500, -4500, 500, -4500, 500, -2000, 500, -2000, 500, -4500, 
            500, -2000, 500, -2000, 500, -2000, 500, -2000, 500, -4500, 500, -39500, 
        ]]

        params = [dict(function=33, toggle=0, device=12)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=33, toggle=0, device=12)
        protocol_base.IrProtocolBase._test_encode(self, params)


Thomson = Thomson()
