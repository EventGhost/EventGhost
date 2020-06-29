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


TIMING = 832


# TODO: finish
class PCTV(protocol_base.IrProtocolBase):
    """
    IR decoder for the PCTV protocol.
    """
    irp = '{38.4k,832,lsb}<-1|1>(2,-8,1,D:8,F:8,2,-100m)'
    frequency = 38400
    bit_count = 48
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 108000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['F', 16, 23],
        ['F_CHECKSUM', 24, 31],
        ['E', 32, 39],
        ['E_CHECKSUM', 40, 47]
    ]
    # [D:0..255,F:0..255]
    encode_parameters = [
        # ['device', 0, 255],
        # ['sub_device', 0, 255],
        # ['function', 0, 255],
        # ['extended_function', 0, 255]
    ]

    def _calc_checksum(self, function, e):
        f = self._invert_bits(function, 8)
        e = self._invert_bits(e, 8)
        return f, e

    def decode(self, data, frequency=0):
        raise DecodeError
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        func_checksum, e_checksum = self._calc_checksum(code.function, code.e)

        if func_checksum != code.f_checksum or e_checksum != code.e_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function, extended_function):
        func_checksum, ex_func_checksum = self._calc_checksum(
            function,
            extended_function
        )

        list(self._get_timing(device, i) for i in range(8)),
        list(self._get_timing(sub_device, i) for i in range(8)),
        list(self._get_timing(function, i) for i in range(8)),
        list(self._get_timing(e, i) for i in range(8)),
        list(self._get_timing(func_checksum, i) for i in range(8)),
        list(self._get_timing(ex_func_checksum, i) for i in range(8)),

        packet = self._build_packet(
            encoded_dev,
            encoded_sub,
            encoded_func,
            encoded_func_check,
            encoded_e,
            encoded_ex_func_check
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        return
        rlc = [[
            1664, -6656, 832, -832, 2496, -832, 3328, -1664, 3328, -832, 1664, -100000,
        ]]

        params = [dict(device=238, function=121)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        return
        params = dict(device=238, function=121)
        protocol_base.IrProtocolBase._test_encode(self, params)


PCTV = PCTV()
