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


TIMING = 406


class DishNetwork(protocol_base.IrProtocolBase):
    """
    IR decoder for the Dish_Network protocol.
    """
    irp = '{57.6k,406,lsb}<1,-7|1,-4>(1,-15,(F:-6,S:5,D:5,1,-15)+)'
    frequency = 57600
    bit_count = 16
    encoding = 'lsb'

    _lead_in = [TIMING, -TIMING * 15]
    _lead_out = [TIMING, -TIMING * 15]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING * 7], [TIMING, -TIMING * 4]]

    _repeat_lead_in = [TIMING, -TIMING * 15]
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['F', 0, 5],
        ['S', 6, 10],
        ['D', 11, 15],
    ]
    # [F:0..63,S:0..31,D:0..31]
    encode_parameters = [
        ['device', 0, 31],
        ['sub_device', 0, 31],
        ['function', 0, 63]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        function = self._reverse_bits(code.function, 6)

        params = dict(
            D=code.device,
            S=code.sub_device,
            F=function,
            frequency=self.frequency
        )

        return protocol_base.IRCode(
            self,
            code.original_rlc,
            code.normalized_rlc,
            params
        )

    def encode(self, device, sub_device, function):
        function = self._reverse_bits(function, 6)

        encoded_dev = list(
            self._get_timing(device, i) for i in range(5)
        )
        encoded_sub = list(
            self._get_timing(sub_device, i) for i in range(5)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(6)
        )

        packet = self._build_packet(
            encoded_func,
            encoded_sub,
            encoded_dev,
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            406, -6090, 406, -1624, 406, -1624, 406, -1624, 406, -1624, 406, -1624, 406, -2842,
            406, -2842, 406, -1624, 406, -2842, 406, -1624, 406, -1624, 406, -1624, 406, -2842,
            406, -1624, 406, -2842, 406, -2842, 406, -6090,
        ]]

        params = [dict(device=5, function=62, sub_device=26)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=5, function=62, sub_device=26)
        protocol_base.IrProtocolBase._test_encode(self, params)


DishNetwork = DishNetwork()
