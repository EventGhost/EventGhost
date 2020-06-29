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


TIMING = 182


class GuangZhou(protocol_base.IrProtocolBase):
    """
    IR decoder for the GuangZhou protocol.
    """
    irp = '{38.0k,182,lsb}<3,-3|3,-6>(20,-10,T:2,D:6,F:8,S:8,20,-10,~T:2,D:6,~F:8,3,^108m,(20,-20,3,^108m)*){T=3}'
    frequency = 38000
    bit_count = 40
    encoding = 'lsb'

    _lead_in = [TIMING * 20, -TIMING * 10]
    _lead_out = [TIMING * 3, 108000]
    _middle_timings = [(TIMING * 20, -TIMING * 10)]
    _bursts = [[TIMING * 3, -TIMING * 3], [TIMING * 3, -TIMING * 6]]

    _repeat_lead_in = [TIMING * 20, -TIMING * 20]
    _repeat_lead_out = [TIMING * 3, 108000]
    _repeat_bursts = []
# T:2,D:6,F:8,S:8,20,-10,~T:2,D:6,~F:8
    _parameters = [
        ['T', 0, 1],
        ['D', 2, 7],
        ['F', 8, 15],
        ['S', 16, 23],
        ['T_CHECKSUM', 24, 25],
        ['D_CHECKSUM', 26, 31],
        ['F_CHECKSUM', 32, 39]

    ]
    # [D:0..63,F:0..255,S:0..255]
    encode_parameters = [
        ['device', 0, 63],
        ['sub_device', 0, 255],
        ['function', 0, 255],
    ]

    def _calc_checksum(self, device, function, toggle):
        f = self._invert_bits(function, 8)
        t = self._invert_bits(toggle, 2)
        return device, f, t

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        dev_checksum, func_checksum, toggle_checksum = self._calc_checksum(code.device, code.function, code.toggle)

        if dev_checksum != code.d_checksum or func_checksum != code.f_checksum or toggle_checksum != code.t_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, sub_device, function):
        toggle = 3

        dev_checksum, func_checksum, toggle_checksum = self._calc_checksum(device, function, toggle)

        encoded_dev = list(
            self._get_timing(device, i) for i in range(6)
        )
        encoded_sub = list(
            self._get_timing(sub_device, i) for i in range(8)
        )
        encoded_func = list(
            self._get_timing(function, i) for i in range(8)
        )
        encoded_toggle = list(
            self._get_timing(toggle, i) for i in range(2)
        )
        encoded_toggle_check = list(
            self._get_timing(toggle_checksum, i) for i in range(2)
        )
        encoded_func_check = list(
            self._get_timing(func_checksum, i) for i in range(8)
        )
        encoded_dev_check = list(
            self._get_timing(dev_checksum, i) for i in range(6)
        )

        packet = self._build_packet(
            encoded_toggle,
            encoded_dev,
            encoded_func,
            encoded_sub,
            self._middle_timings,
            encoded_toggle_check,
            encoded_dev_check,
            encoded_func_check
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            3640, -1820, 546, -1092, 546, -1092, 546, -546, 546, -546, 546, -1092, 546, -546, 546, -1092,
            546, -546, 546, -546, 546, -546, 546, -1092, 546, -546, 546, -546, 546, -546, 546, -546, 546, -546,
            546, -546, 546, -1092, 546, -1092, 546, -546, 546, -546, 546, -1092, 546, -1092, 546, -546,
            3640, -1820, 546, -546, 546, -546, 546, -546, 546, -546, 546, -1092, 546, -546, 546, -1092, 546, -546,
            546, -1092, 546, -1092, 546, -546, 546, -1092, 546, -1092, 546, -1092, 546, -1092, 546, -1092, 546, -43026
        ]]
        params = [dict(device=20, function=4, sub_device=102)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=20, function=4, sub_device=102)
        protocol_base.IrProtocolBase._test_encode(self, params)


GuangZhou = GuangZhou()
