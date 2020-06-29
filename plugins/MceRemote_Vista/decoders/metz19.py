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


TIMING = 106


class Metz19(protocol_base.IrProtocolBase):
    """
    IR decoder for the Metz19 protocol.
    """
    irp = '{37.9k,106,msb}<4,-9|4,-16>(8,-22,(1-T):1,D:3,~D:3,F:6,~F:6,4,-125m)*'
    frequency = 37900
    bit_count = 19
    encoding = 'msb'

    _lead_in = [TIMING * 8, -TIMING * 22]
    _lead_out = [TIMING * 4, -125000]
    _middle_timings = []
    _bursts = [[TIMING * 4, -TIMING * 9], [TIMING * 4, -TIMING * 16]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['T', 0, 0],
        ['D', 1, 3],
        ['D_CHECKSUM', 4, 6],
        ['F', 7, 12],
        ['F_CHECKSUM', 13, 18],
    ]
    # [D:0..7,F:0..63,T@:0..1=0]
    encode_parameters = [
        ['device', 0, 7],
        ['function', 0, 63],
        ['toggle', 0, 1]
    ]

    def _calc_checksum(self, device, function):
        d = self._invert_bits(device, 3)
        f = self._invert_bits(function, 6)
        return d, f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        dev_checksum, func_checksum = self._calc_checksum(code.device, code.function)

        if dev_checksum != code.d_checksum or func_checksum != code.f_checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function, toggle):
        toggle = 1-toggle

        dev_checksum, func_checksum = self._calc_checksum(
            device,
            function,
        )

        packet = self._build_packet(
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(3)),
            list(self._get_timing(dev_checksum, i) for i in range(3)),
            list(self._get_timing(function, i) for i in range(6)),
            list(self._get_timing(func_checksum, i) for i in range(6))
        )

        return self.decode(packet, self.frequency)

    def _test_decode(self):
        rlc = [[
            848, -2332, 424, -1696, 424, -954, 424, -1696, 424, -1696, 424, -1696, 424, -954, 
            424, -954, 424, -954, 424, -954, 424, -954, 424, -954, 424, -954, 424, -954, 
            424, -1696, 424, -1696, 424, -1696, 424, -1696, 424, -1696, 424, -1696, 424, -125000, 
        ]]

        params = [dict(function=0, toggle=1, device=3)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=0, toggle=1, device=3)
        protocol_base.IrProtocolBase._test_encode(self, params)


Metz19 = Metz19()
