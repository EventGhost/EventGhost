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


TIMING = 872


class Emerson(protocol_base.IrProtocolBase):
    """
    IR decoder for the Emerson protocol.
    """
    irp = '{36.7k,872,lsb}<1,-1|1,-3>(4,-4,D:6,F:6,~D:6,~F:6,1,-39)*'
    frequency = 36700
    bit_count = 24
    encoding = 'lsb'

    _lead_in = [TIMING * 4, -TIMING * 4]
    _lead_out = [TIMING, -TIMING * 39]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 5],
        ['F', 6, 11],
        ['D_CHECKSUM', 12, 17],
        ['F_CHECKSUM', 18, 23],
    ]
    # [D:0..63,F:0..63]
    encode_parameters = [
        ['device', 0, 63],
        ['function', 0, 63],
    ]

    def _calc_checksum(self, device, function):
        d = self._invert_bits(device, 6)
        f = self._invert_bits(function, 6)
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
            function,
        )

        encoded_dev = list(
            self._get_timing(device, i) for i in range(6)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(6)
        )
        encoded_dev_check = list(
            self._get_timing(dev_checksum, i) for i in range(6)
        )
        encoded_func_check = list(
            self._get_timing(func_checksum, i) for i in range(6)
        )

        packet = self._build_packet(
            encoded_dev,
            encoded_func,
            encoded_dev_check,
            encoded_func_check,
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3488, -3488, 872, -872, 872, -872, 872, -872, 872, -872, 872, -872, 872, -2616,
            872, -2616, 872, -2616, 872, -872, 872, -872, 872, -872, 872, -2616, 872, -2616,
            872, -2616, 872, -2616, 872, -2616, 872, -2616, 872, -872, 872, -872, 872, -872,
            872, -2616, 872, -2616, 872, -2616, 872, -872, 872, -34008,
        ]]

        params = [dict(device=32, function=35)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=32, function=35)
        protocol_base.IrProtocolBase._test_encode(self, params)


Emerson = Emerson()
