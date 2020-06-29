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


TIMING = 833


class PanasonicOld(protocol_base.IrProtocolBase):
    """
    IR decoder for the PanasonicOld protocol.
    """
    irp = '{57.6k,833,lsb}<1,-1|1,-3>(4,-4,D:5,F:6,~D:5,~F:6,1,-44m)*'
    frequency = 57600
    bit_count = 22
    encoding = 'lsb'

    _lead_in = [TIMING * 4, -TIMING * 4]
    _lead_out = [TIMING, -44000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 4],
        ['F', 5, 10],
        ['D_CHECKSUM', 11, 15],
        ['F_CHECKSUM', 16, 21],
    ]
    # [D:0..31,F:0..63]
    encode_parameters = [
        ['device', 0, 31],
        ['function', 0, 63],
    ]

    def _calc_checksum(self, device, function):
        f = self._invert_bits(function, 6)
        d = self._invert_bits(device, 5)
        return d, f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        dev_checksum, func_checksum = self._calc_checksum(code.device, code.function)

        if func_checksum != code.f_checksum or dev_checksum != code.d_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function):
        dev_checksum, func_checksum = self._calc_checksum(
            device,
            function,
        )

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(5)),
            list(self._get_timing(function, i) for i in range(6)),
            list(self._get_timing(dev_checksum, i) for i in range(5)),
            list(self._get_timing(func_checksum, i) for i in range(6))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            3332, -3332, 833, -833, 833, -2499, 833, -833, 833, -833, 833, -2499, 833, -833, 
            833, -2499, 833, -833, 833, -2499, 833, -2499, 833, -833, 833, -2499, 833, -833, 
            833, -2499, 833, -2499, 833, -833, 833, -2499, 833, -833, 833, -2499, 833, -833, 
            833, -833, 833, -2499, 833, -44000, 
        ]]

        params = [dict(device=18, function=26)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=18, function=26)
        protocol_base.IrProtocolBase._test_encode(self, params)


PanasonicOld = PanasonicOld()
