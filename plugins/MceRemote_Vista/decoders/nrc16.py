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
from . import (
    DecodeError,
    RepeatLeadIn,
    RepeatLeadOut,
    RepeatTimeoutExpired
)
import time

TIMING = 500


class NRC16(protocol_base.IrProtocolBase):
    """
    IR decoder for the NRC16 protocol.
    """
    irp = '{38k,500,lsb}<-1,1|1,-1>(1,-5,1:1,254:8,127:7,-15m,(1,-5,1:1,F:8,D:7,-110m)+,1,-5,1:1,254:8,127:7,-15m)'
    frequency = 38000
    bit_count = 16
    encoding = 'lsb'

    _lead_in = [TIMING, -TIMING * 5]
    _lead_out = [-15000]
    _middle_timings = []
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['F', 1, 8],
        ['D', 9, 15]
    ]
    # [D:0..127,F:0..255]
    encode_parameters = [
        ['device', 0, 127],
        ['function', 0, 255],
    ]

    repeat_timeout = 129500

    def reset(self):
        self._lead_out = [-15000]
        self._last_code = None

    def decode(self, data, frequency=0):
        try:
            code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        except DecodeError:
            self._lead_out = [-15000]
            try:
                code = protocol_base.IrProtocolBase.decode(self, data, frequency)
            except DecodeError:
                self.reset()
                raise

        if code.c0 != 1:
            self.reset()
            raise DecodeError('Invalid checksum')

        if code.device == 127 and code.function == 254:
            if self._last_code is None:
                self._lead_out = [-110000]
                raise RepeatLeadIn
            else:
                self._last_code.repeat_timer.stop()
                self.reset()
                raise RepeatLeadOut
        else:
            if self._last_code is None:
                self._last_code = code
                code.repeat_timer.start()
                return code

            if not self._last_code.repeat_timer.is_running:
                raise RepeatTimeoutExpired

            if self._last_code != code:
                raise DecodeError('Repeat code does not match last code')

            self._last_code.repeat_timer.start()
            return self._last_code

    def encode(self, device, function):
        lead_out = self._lead_out

        self._lead_out = [-15000]

        c0 = 1
        f = 254
        d = 127

        prefix = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(f, i) for i in range(8)),
            list(self._get_timing(d, i) for i in range(7))
        )

        suffix = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(f, i) for i in range(8)),
            list(self._get_timing(d, i) for i in range(7))
        )

        self._lead_out = [-110000]

        code = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(function, i) for i in range(8)),
            list(self._get_timing(device, i) for i in range(7))
        )

        self._lead_out = lead_out

        return [prefix, code, suffix]

    def _test_decode(self):
        rlc_codes = [
            [
                +500, -2500, +500, -1000, +1000, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -500,
                +500, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -15500
            ],
            [
                +500, -2500, +500, -1000, +1000, -1000, +1000, -500, +500, -500, +500, -500, +500, -1000,
                +1000, -500, +500, -500, +500, -500, +500, -1000, +500, -500, +500, -500, +500, -110000
            ],
            [
                +500, -2500, +500, -1000, +1000, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -500,
                +500, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -500, +500, -15500
            ]
        ]

        params = [
            dict(device=127, function=254),
            dict(device=15, function=122),
            dict(device=127, function=254),
        ]

        protocol_base.IrProtocolBase._test_decode(self, rlc_codes, params)

    def _test_encode(self):
        params = dict(device=15, function=122)
        protocol_base.IrProtocolBase._test_encode(self, params)


NRC16 = NRC16()
