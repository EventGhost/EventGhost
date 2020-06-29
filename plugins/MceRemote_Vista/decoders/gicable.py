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


TIMING = 490


class GICable(protocol_base.IrProtocolBase):
    """
    IR decoder for the GICable protocol.
    """
    irp = '{38.7k,490,lsb}<1,-4.5|1,-9>(18,-9,F:8,D:4,C:4,1,-84,(18,-4.5,1,-178)*){C=-(D+F:4+F:4:4)}'
    frequency = 38700
    bit_count = 16
    encoding = 'lsb'

    _lead_in = [TIMING * 18, -TIMING * 9]
    _lead_out = [TIMING, -TIMING * 84]
    _middle_timings = []
    _bursts = [[TIMING, int(round(-TIMING * 4.5))], [TIMING, -TIMING * 9]]

    _repeat_lead_in = [TIMING * 18, int(round(-TIMING * 4.5))]
    _repeat_lead_out = [TIMING, -TIMING * -178]
    _repeat_bursts = []

    _parameters = [
        ['F', 0, 7],
        ['D', 8, 11],
        ['CHECKSUM', 12, 15]
    ]
    # [D:0..15,F:0..255]
    encode_parameters = [
        ['device', 0, 15],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, device, function):
        # -(D+F:4+F:4:4)
        f1 = self._get_bits(function, 0, 3)
        f2 = self._get_bits(function, 4, 7)

        c = -(device + f1 + f2)
        return self._get_bits(c, 0, 3)

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.device, code.function)

        if checksum != code.checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        checksum = self._calc_checksum(device, function)

        encoded_dev = list(
            self._get_timing(device, i) for i in range(4)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )
        encoded_checksum = list(
            self._get_timing(checksum, i) for i in range(4)
        )

        packet = self._build_packet(
            encoded_func,
            encoded_dev,
            encoded_checksum
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            8820, -4410, 490, -2205, 490, -2205, 490, -2205, 490, -4410, 490, -2205, 490, -4410, 490, -4410,
            490, -4410, 490, -2205, 490, -2205, 490, -2205, 490, -2205, 490, -2205, 490, -4410, 490, -2205,
            490, -4410, 490, -41160
        ]]

        params = [dict(device=0, function=232)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=0, function=232)
        protocol_base.IrProtocolBase._test_encode(self, params)


GICable = GICable()
