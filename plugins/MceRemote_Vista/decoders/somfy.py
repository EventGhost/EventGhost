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


class Somfy(protocol_base.IrProtocolBase):
    """
    IR decoder for the Somfy protocol.
    """
    irp = '{35.7k,1,lsb}<308,-881|669,-520>(2072,-484,F:2,D:3,C:4,-2300)*{C=F*4+D+3}'
    frequency = 35700
    bit_count = 9
    encoding = 'lsb'

    _lead_in = [2072, -484]
    _lead_out = [-2300]
    _middle_timings = []
    _bursts = [[308, -881], [669, -520]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['F', 0, 1],
        ['D', 2, 4],
        ['CHECKSUM', 5, 8]
    ]
    # [F:0..3,D:0..7]
    encode_parameters = [
        ['device', 0, 7],
        ['function', 0, 3],
    ]

    def _calc_checksum(self, device, function):
        # {C=F*4+D+3}
        return self._get_bits(function * 4 + device + 3, 0, 3)

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.device, code.function)

        if checksum != code.checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        checksum = self._calc_checksum(device, function)

        packet = self._build_packet(
            list(self._get_timing(function, i) for i in range(2)),
            list(self._get_timing(device, i) for i in range(3)),
            list(self._get_timing(checksum, i) for i in range(4)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            2072, -484, 669, -520, 669, -520, 308, -881, 669, -520, 308, -881, 669, -520, 
            308, -881, 308, -881, 308, -3181, 
        ]]

        params = [dict(device=2, function=3)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=2, function=3)
        protocol_base.IrProtocolBase._test_encode(self, params)


Somfy = Somfy()

