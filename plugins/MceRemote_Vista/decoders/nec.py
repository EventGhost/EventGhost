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


TIMING = 564


class NEC(protocol_base.IrProtocolBase):
    """
    IR decoder for the NEC protocol.
    """
    irp = '{38.4k,564,lsb}<1,-1|1,-3>(16,-8,D:8,S:8,F:8,~F:8,1,^108m,(16,-4,1,^108m)*)'
    frequency = 38400
    bit_count = 32
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 108000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 4]
    _repeat_lead_out = [TIMING, 108000]
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['F', 16, 23],
        ['F_CHECKSUM', 24, 31],
    ]
    # [D:0..255,S:0..255=255-D,F:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['sub_device', 0, 255],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, function):
        f = self._invert_bits(function, 8)
        return f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        func_checksum = self._calc_checksum(code.function)

        if func_checksum != code.f_checksum:
            raise DecodeError('Checksum failed')

        params = dict(
            D=code.device,
            S=code.sub_device,
            F=code.function,
            F_CHECKSUM=code.f_checksum,
            frequency=self.frequency
        )

        return protocol_base.IRCode(
            self,
            code.original_rlc,
            code.normalized_rlc,
            params
        )

    def encode(self, device, sub_device, function):
        func_checksum = self._calc_checksum(function)

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(func_checksum, i) for i in range(8)),
        )

        return packet

    def _test_decode(self):
        rlc = [[
            9024, -4512, 564, -564, 564, -1692, 564, -1692, 564, -1692, 564, -564, 564, -1692, 564, -564,
            564, -564, 564, -564, 564, -564, 564, -1692, 564, -564, 564, -1692, 564, -1692, 564, -564,
            564, -564, 564, -1692, 564, -564, 564, -564, 564, -564, 564, -564, 564, -1692, 564, -1692,
            564, -564, 564, -564, 564, -1692, 564, -1692, 564, -1692, 564, -1692, 564, -564, 564, -564,
            564, -1692, 564, -40884
        ]]

        params = [dict(function=97, sub_device=52, device=46)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=97, sub_device=52, device=46)
        protocol_base.IrProtocolBase._test_encode(self, params)


NEC = NEC()
