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


TIMING = 300


class MCIR2kbd(protocol_base.IrProtocolBase):
    """
    IR decoder for the MCIR2kbd protocol.
    """
    irp = (
        '{0k,300,msb}<-1,1|1,-1>(9,32:8,C:5,0:8,F:8,M:8,-74m)*'
        '{c1=#(F&0b11111000)%2,'
        'c2=(#(F&0b00000111)+#(M&0b00110000))%2,'
        'c3=(#(F&0b11000111)+#(M&0b10001110))%2,'
        'c4=(#(F&0b00110110)+#(M&0b10101101))%2,'
        'c5=(#(F&0b10101101)+#(M&0b10011011))%2,'
        'C=(c1<<4)|(c2<<3)|(c3<<2)|(c4<<1)|c5}'
    )
    frequency = 0
    bit_count = 37
    encoding = 'msb'

    _lead_in = [TIMING * 9]
    _lead_out = [-74000]
    _middle_timings = []
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 7],
        ['CHECKSUM', 8, 12],
        ['C1', 13, 20],
        ['F', 21, 28],
        ['M', 29, 36]
    ]
    # [F:0..255,M:0..255]
    encode_parameters = [
        ['function', 0, 255],
        ['mode', 0, 255]
    ]

    def _calc_checksum(self, function, mode):
        # c1=#(F&0b11111000)%2,
        # c2=(#(F&0b00000111)+#(M&0b00110000))%2,
        # c3=(#(F&0b11000111)+#(M&0b10001110))%2,
        # c4=(#(F&0b00110110)+#(M&0b10101101))%2,
        # c5=(#(F&0b10101101)+#(M&0b10011011))%2,
        # C=(c1<<4)|(c2<<3)|(c3<<2)|(c4<<1)|c5}
        
        c1 = self._count_one_bits(function & 0b11111000) % 2
        c2 = (self._count_one_bits(function & 0b00000111) + self._count_one_bits(mode & 0b00110000)) % 2
        c3 = (self._count_one_bits(function & 0b11000111) + self._count_one_bits(mode & 0b10001110)) % 2
        c4 = (self._count_one_bits(function & 0b00110110) + self._count_one_bits(mode & 0b10101101)) % 2
        c5 = (self._count_one_bits(function & 0b10101101) + self._count_one_bits(mode & 0b10011011)) % 2

        c = (c1 << 4) | (c2 << 3) | (c3 << 2) | (c4 << 1) | c5

        return c

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        checksum = self._calc_checksum(code.function, code.mode)

        if checksum != code.checksum or code.c0 != 32 or code.c1 != 0:
            raise DecodeError('Checksum failed')

        return code

    def encode(self, function, mode):
        c0 = 32
        c1 = 0

        checksum = self._calc_checksum(
            function,
            mode
        )

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(8)),
            list(self._get_timing(checksum, i) for i in range(5)),
            list(self._get_timing(c1, i) for i in range(8)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(mode, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):
        rlc = [[
            2700, -300, 300, -300, 600, -600, 300, -300, 300, -300, 300, -300, 300, -300, 
            300, -300, 600, -600, 300, -300, 600, -600, 300, -300, 300, -300, 300, -300, 300, -300, 
            300, -300, 300, -300, 300, -300, 600, -600, 600, -300, 300, -300, 300, -300, 300, -300, 
            300, -300, 300, -600, 300, -300, 600, -300, 300, -600, 300, -300, 300, -300, 
            600, -74300, 
        ]]

        params = [dict(function=191, mode=49)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=191, mode=49)
        protocol_base.IrProtocolBase._test_encode(self, params)


MCIR2kbd = MCIR2kbd()
