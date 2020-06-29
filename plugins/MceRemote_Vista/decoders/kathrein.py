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


TIMING = 540


class Kathrein(protocol_base.IrProtocolBase):
    """
    IR decoder for the Kathrein protocol.
    """
    irp = '{38k,540,lsb}<1,-1|1,-3>(16,-8,D:4,~D:4,F:8,~F:8,1,^105m,(16,-8,F:8,1,^105m)+)'
    frequency = 38000
    bit_count = 24
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 105000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 8]
    _repeat_lead_out = [TIMING, 105000]
    _repeat_bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

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
            function,
        )

        encoded_dev = list(
            self._get_timing(device, i) for i in range(4)
        )
        encoded_dev_check = list(
            self._get_timing(dev_checksum, i) for i in range(4)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )

        encoded_func_check = list(
            self._get_timing(func_checksum, i) for i in range(8)
        )


        packet = self._build_packet(
            encoded_dev,
            encoded_dev_check,
            encoded_func,
            encoded_func_check,
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            8640, -4320, 540, -540, 540, -540, 540, -1620, 540, -540, 540, -1620, 540, -1620, 540, -540,
            540, -1620, 540, -1620, 540, -540, 540, -540, 540, -1620, 540, -540, 540, -1620, 540, -540,
            540, -540, 540, -540, 540, -1620, 540, -1620, 540, -540, 540, -1620, 540, -540, 540, -1620,
            540, -1620, 540, -52620
        ]]

        params = [dict(device=4, function=41)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=4, function=41)
        protocol_base.IrProtocolBase._test_encode(self, params)


Kathrein = Kathrein()
