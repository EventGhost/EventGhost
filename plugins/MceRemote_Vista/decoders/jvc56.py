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

TIMING = 432


class JVC56(protocol_base.IrProtocolBase):
    """
    IR decoder for the JVC56 protocol.
    """
    irp = '{37k,432,lsb}<1,-1|1,-3>(8,-4,3:8,1:8,D:8,S:8,X:8,F:8,(D^S^X^F):8,1,-173)*'
    frequency = 37000
    bit_count = 56
    encoding = 'lsb'

    _lead_in = [TIMING * 8, -TIMING * 4]
    _lead_out = [TIMING, -TIMING * 173]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 7],
        ['C1', 8, 15],
        ['D', 16, 23],
        ['S', 24, 31],
        ['X', 32, 39],
        ['F', 40, 47],
        ['CHECKSUM', 48, 55]
    ]
    # [D:0..255,S:0..255,F:0..255,X:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['sub_device', 0, 255],
        ['function', 0, 255],
        ['x', 0, 255]
    ]

    def _calc_checksum(self, device, sub_device, function, x):
        return device ^ sub_device ^ function ^ x

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.device, code.sub_device, code.function, code.x)

        if checksum != code.checksum or code.c0 != 3 or code.c1 != 1:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function, x):
        c0 = 3
        c1 = 1
        checksum = self._calc_checksum(
            device,
            sub_device,
            function,
            x
        )

        encoded_dev = list(
            self._get_timing(device, i) for i in range(8)
        )
        encoded_sub = list(
            self._get_timing(sub_device, i) for i in range(8)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )
        encoded_x = list(
            self._get_timing(x, i) for i in range(8)
        )
        encoded_checksum = list(
            self._get_timing(checksum, i) for i in range(8)
        )
        encoded_c0 = list(
            self._get_timing(c0, i) for i in range(8)
        )
        encoded_c1 = list(
            self._get_timing(c1, i) for i in range(8)
        )

        packet = self._build_packet(
            encoded_c0,
            encoded_c1,
            encoded_dev,
            encoded_sub,
            encoded_x,
            encoded_func,
            encoded_checksum
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3456, -1728, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432,
            432, -1296, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -432, 432, -1296,
            432, -432, 432, -432, 432, -432, 432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -1296, 432, -432,
            432, -1296, 432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -432, 432, -432, 432, -1296,
            432, -432, 432, -432, 432, -1296, 432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -1296,
            432, -432, 432, -1296, 432, -1296, 432, -432, 432, -1296, 432, -1296, 432, -1296, 432, -432, 432, -432,
            432, -432, 432, -432, 432, -432, 432, -74736
        ]]

        params = [dict(device=225, function=111, sub_device=237, x=100)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=225, function=111, sub_device=237, x=100)
        protocol_base.IrProtocolBase._test_encode(self, params)


JVC56 = JVC56()
