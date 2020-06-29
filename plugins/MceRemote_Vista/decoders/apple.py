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


class Apple(protocol_base.IrProtocolBase):
    """
    IR decoder for the Apple protocol.
    """
    irp = (
        '{38.4k,564,lsb}<1,-1|1,-3>(16,-8,D:8,S:8,C:1,F:7,PairID:8,1,^108m,(16,-4,1,^108m)*)'
        '{C=1-(#F+#PairID)%2,S=135}'
    )
    frequency = 38400
    bit_count = 32
    encoding = 'lsb'

    _lead_in = [TIMING * 16, -TIMING * 8]
    _lead_out = [TIMING, 108000]
    _bursts = [[TIMING, -TIMING], [TIMING, -TIMING * 3]]

    _repeat_lead_in = [TIMING * 16, -TIMING * 4]
    _repeat_lead_out = [TIMING, 108000]
    _repeat_bursts = []

    _parameters = [
        ['D', 0, 7],
        ['S', 8, 15],
        ['CHECKSUM', 16, 16],
        ['F', 17, 23],
        ['PAIR_ID', 24, 31]
    ]
    # [D:0..255=238,F:0..127,PairID:0..255]
    encode_parameters = [
        ['device', 0, 255],
        ['function', 0, 127],
        ['pair_id', 0, 255]
    ]

    def _calc_checksum(self, function, pair_id):
        c = 1 - (self._count_one_bits(function) + self._count_one_bits(pair_id)) % 2
        return c

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.function, code.pair_id)

        if code.sub_device != 135 or checksum != code.checksum:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, device, function, pair_id):
        sub_device = 135
        checksum = self._calc_checksum(function, pair_id)

        packet = self._build_packet(
            list(self._get_timing(device, i) for i in range(8)),
            list(self._get_timing(sub_device, i) for i in range(8)),
            list(self._get_timing(checksum, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(7)),
            list(self._get_timing(pair_id, i) for i in range(8))
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            9024, -4512, 564, -1692, 564, -564, 564, -1692, 564, -1692, 564, -564, 564, -1692, 564, -564,
            564, -564, 564, -1692, 564, -1692, 564, -1692, 564, -564, 564, -564, 564, -564, 564, -564,
            564, -1692, 564, -564, 564, -564, 564, -1692, 564, -564, 564, -1692, 564, -564, 564, -564,
            564, -564, 564, -1692, 564, -564, 564, -564, 564, -564, 564, -1692, 564, -1692, 564, -1692,
            564, -1692, 564, -40884
        ]]

        params = [dict(device=45, function=10, pair_id=241)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=45, function=10, pair_id=241)
        protocol_base.IrProtocolBase._test_encode(self, params)


Apple = Apple()

