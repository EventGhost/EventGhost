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


TIMING = 512


# [ 512, -512,   512, -512,   512, -512,   512, -512,   512, -512,   512, -512,   512, -512,   512, -512,   512, -512,   512, 512]
# [[512, -512], [512, -512], [512, -512], [512, -512], [512, -512], [512, -512], [512, -512], [512, -512], [512, -512], [512, 512]]
class Blaupunkt(protocol_base.IrProtocolBase):
    """
    IR decoder for the Blaupunkt protocol.
    """
    irp = '{30.3k,512,lsb}<-1,1|1,-1>(1,-5,1023:10,-44,(1,-5,1:1,F:6,D:3,-236)+,1,-5,1023:10,-44)'
    frequency = 30300
    bit_count = 10
    encoding = 'lsb'

    _lead_in = [TIMING, -TIMING * 5]
    _lead_out = [-TIMING * 44]
    _middle_timings = []
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['F', 1, 6],
        ['D', 7, 9]
    ]
    # [F:0..63,D:0..7]
    encode_parameters = [
        ['device', 0, 7],
        ['function', 0, 63],
    ]

    def __init__(self):
        self.packet_count = 0
        protocol_base.IrProtocolBase.__init__(self)

    def decode(self, data, frequency=0):

        try:
            code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        except DecodeError:
            self._lead_out[0] = -TIMING * 44
            try:
                code = protocol_base.IrProtocolBase.decode(self, data, frequency)
            except DecodeError:
                self.reset()
                raise

        if self._lead_out[0] == -TIMING * 44:
            if code.c0 != 1 or code.device != 7 or code.function != 63:
                if self._last_code is None:
                    raise DecodeError('Invalid repeat lead in')
                else:
                    self.reset()
                    raise DecodeError('Invalid repeat lead out')

            if self._last_code is None:
                self._lead_out[0] = -TIMING * 236
                raise RepeatLeadIn

            else:
                self.reset()
                raise RepeatLeadOut

        if code.c0 != 1:
            raise DecodeError('Invalid checksum')

        if self._last_code is None:
            self._last_code = code
            code.repeat_timer.start()
            return code

        if self._last_code != code:
            raise DecodeError('Repeat code does not match')

        if self._last_code.repeat_timer.is_running:
            self._last_code.repeat_timer.cancel()
            self._last_code.repeat_timer.start()
            return self._last_code

        self.reset()
        raise RepeatTimeoutExpired

    def encode(self, device, function):
        c0 = 1
        d = 7
        f = 63

        _lead_out = self._lead_out[0]

        self._lead_out[0] = -TIMING * 44

        lead_in = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(d, i) for i in range(3)),
            list(self._get_timing(f, i) for i in range(6))
        )

        self._lead_out[0] = -TIMING * 236

        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(3)),
            list(self._get_timing(function, i) for i in range(6))
        )

        self._lead_out[0] = -TIMING * 44

        lead_out = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(d, i) for i in range(3)),
            list(self._get_timing(f, i) for i in range(6))
        )

        self._lead_out[0] = _lead_out

        return [lead_in, packet, lead_out]

    def _test_decode(self):
        rlc = [
            [
                +512, -2560, +512, -512, +512, -512, +512, -512, +512, -512, +512, -512, +512, -512, +512, -512, +512,
                -512, +512, -512, +512, -23040
            ],
            [
                +512, -2560, +512, -512, +512, -1024, +1024, -1024, +512, -512, +512, -512, +1024, -512, +512, -1024,
                +512, -120832
            ],
            [
                +512, -2560, +512, -512, +512, -512, +512, -512, +512, -512, +512, -512, +512, -512, +512, -512, +512,
                -512, +512, -512, +512, -23040
            ],
        ]

        params = [
            None,
            dict(device=3, function=5),
            None
        ]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=3, function=5)
        protocol_base.IrProtocolBase._test_encode(self, params)


Blaupunkt = Blaupunkt()
