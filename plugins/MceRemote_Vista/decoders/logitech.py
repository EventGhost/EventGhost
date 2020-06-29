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


TIMING = 127


class Logitech(protocol_base.IrProtocolBase):
    """
    IR decoder for the Logitech protocol.
    """
    irp = '{38k,127,lsb}<3,-4|3,-8>(31,-36,D:4,~D:4,F:8,~F:8,3,-50m)*'
    frequency = 38000
    bit_count = 24
    encoding = 'lsb'

    _lead_in = [TIMING * 31, -TIMING * 36]
    _lead_out = [TIMING * 3, -50000]
    _middle_timings = []
    _bursts = [[TIMING * 3, -TIMING * 4], [TIMING * 3, -TIMING * 8]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 3],
        ['D_CHECKSUM', 4, 7],
        ['F', 8, 15],
        ['F_CHECKSUM', 16, 23],
    ]
    # [D:0..15,F:0..255]
    encode_parameters = [
        ['device', 0, 15],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, device, function):
        d = self._invert_bits(device, 4)
        f = self._invert_bits(function, 8)
        return d, f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        dev_checksum, func_checksum = self._calc_checksum(code.device, code.function)

        if dev_checksum != code.d_checksum or func_checksum != code.f_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        dev_checksum, func_checksum = self._calc_checksum(
            device,
            function
        )

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(4)),
            list(self._get_timing(dev_checksum, i) for i in range(4)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(func_checksum, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            3937, -4572, 381, -1016, 381, -1016, 381, -1016, 381, -508, 381, -508, 381, -508, 381, -508,
            381, -1016, 381, -1016, 381, -508, 381, -508, 381, -508, 381, -508, 381, -1016, 381, -508,
            381, -1016, 381, -508, 381, -1016, 381, -1016, 381, -1016, 381, -1016, 381, -508, 381, -1016,
            381, -508, 381, -50000
        ]]

        params = [dict(device=7, function=161)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=7, function=161)
        protocol_base.IrProtocolBase._test_encode(self, params)


Logitech = Logitech()
