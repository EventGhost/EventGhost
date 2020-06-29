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


TIMING = 388

BIT_MAPPING = {
    0: 1,
    2: 2,
    8: 3,
    10: 4,
    32: 5,
    34: 6,
    40: 7,
    42: 8,
    128: 9,
    130: 10,
    136: 11,
    138: 12,
    160: 13,
    162: 14,
    168: 15,
    170: 16,
}


class Arctech(protocol_base.IrProtocolBase):
    """
    IR decoder for the Arctech protocol.
    """
    irp = '{0k,388,lsb}<1,-3|3,-1>(<0:2|2:2>((D-1):4,(S-1):4),40:7,F:1,0:1,-10.2m)*'
    frequency = 0
    bit_count = 25
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 108000]
    _bursts = [[TIMING, -TIMING * 3], [TIMING * 3, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['C0', 16, 22],
        ['F', 23, 23],
        ['C1', 24, 24],
    ]
    # [D:1..16,S:1..16,F:0..1]
    encode_parameters = [
        ['device', 1, 16],
        ['sub_device', 1, 16],
        ['function', 0, 1],
    ]

    def decode(self, data, frequency=0):
        raise DecodeError
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 40 or code.c1 != 0:
            raise DecodeError('Checksum failed')

        device = BIT_MAPPING[code.device]
        sub_device = BIT_MAPPING[code.sub_device]

        params = {
            'D': device,
            'S': sub_device,
            'C0': code.c0,
            'F': code.function,
            'C1': code.c1,
            'frequency': self.frequency
        }

        return protocol_base.IRCode(
            self.__class__.__name__,
            code.original_code,
            code.normalized_code,
            params
        )

    def encode(self, device, sub_device, function):
        c0 = 40
        c1 = 0

        bit_mapping = {v: k for k, v in BIT_MAPPING.items()}

        device = bit_mapping[device - 1]
        sub_device = bit_mapping[sub_device - 1]

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(c0, i) for i in range(7)),
            list(self._get_timing(function, i) for i in range(1)),
            list(self._get_timing(c1, i) for i in range(1)),
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        return
        rlc = [[
            388, -1164, 388, -1164, 388, -1164, 1164, -388, 388, -1164, 1164, -388, 388, -1164, 388, -1164,
            388, -1164, 388, -1164, 388, -1164, 388, -1164, 388, -1164, 1164, -388, 388, -1164, 1164, -388,
            388, -1164, 388, -1164, 388, -1164, 1164, -388, 388, -1164, 1164, -388, 388, -1164, 388, -1164,
            388, -11364
        ]]

        params = [dict(device=7, function=0, sub_device=13)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        return
        params = dict(device=7, function=0, sub_device=13)
        protocol_base.IrProtocolBase._test_encode(self, params)


Arctech = Arctech()
