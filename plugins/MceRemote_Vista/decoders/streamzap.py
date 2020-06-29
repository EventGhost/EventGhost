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

STREAMZAP = {
    0x00: "Num0",
    0x01: "Num1",
    0x02: "Num2",
    0x03: "Num3",
    0x04: "Num4",
    0x05: "Num5",
    0x06: "Num6",
    0x07: "Num7",
    0x08: "Num8",
    0x09: "Num9",
    0x0A: "Power",
    0x0B: "Mute",
    0x0C: "ChannelUp",
    0x0D: "VolumeUp",
    0x0E: "ChannelDown",
    0x0F: "VolumeDown",
    0x10: "Up",
    0x11: "Left",
    0x12: "Ok",
    0x13: "Right",
    0x14: "Down",
    0x15: "Menu",
    0x16: "Exit",
    0x17: "Play",
    0x18: "Pause",
    0x19: "Stop",
    0x1A: "PreviousTrack",
    0x1B: "NextTrack",
    0x1C: "Record",
    0x1D: "Rewind",
    0x1E: "Forward",
    0x20: "Red",
    0x21: "Green",
    0x22: "Yellow",
    0x23: "Blue",
}

TIMING = 889


class StreamZap(protocol_base.IrProtocolBase):
    """
    IR decoder for the StreamZap protocol.
    """
    irp = '{36k,889,msb}<1,-1|-1,1>(1,~F:1:6,T:1,D:6,F:6,^114m)*'
    frequency = 36000
    bit_count = 14
    encoding = 'msb'

    _lead_in = [TIMING]
    _lead_out = [114000]
    _middle_timings = []
    _bursts = [[TIMING, -TIMING], [-TIMING, TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['F_CHECKSUM', 0, 0],
        ['T', 1, 1],
        ['D', 2, 7],
        ['F', 8, 13]
    ]
    # [D:0..63,F:0..63,T:0..1]
    encode_parameters = [
        ['device', 0, 63],
        ['function', 0, 63],
        ['toggle', 0, 1]
    ]

    def _calc_checksum(self, function):
        f = int(not self._get_bit(function, 5))
        return f

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)
        func_checksum = self._calc_checksum(code.function)

        if func_checksum != code.f_checksum:
            raise DecodeError('Checksum failed')

        if code.function in STREAMZAP:
            code.name = '{0}.{1}.{2}'.format(
                self.__class__.__name__,
                hex(code.device)[2:].upper().zfill(2),
                STREAMZAP[code.function]
            )

        return code

    def encode(self, device, function, toggle):
        func_checksum = self._calc_checksum(function)
        packet = self._build_packet(
            list(self._get_timing(func_checksum, i) for i in range(1)),
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(6)),
            list(self._get_timing(function, i) for i in range(6)),
        )

        return [packet]

    def _test_decode(self):
        import random

        packets = []

        for function in range(0x00, 0x24):
            if function == 0x2F:
                continue

            device = random.randrange(0, 63)
            toggle = 1

            rlc = self.encode(device, function, toggle)
            params = [dict(device=device, function=function, toggle=toggle)]

            packets += [[rlc, params]]

        for rlc, params in packets:
            protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=10, toggle=1, device=51)
        protocol_base.IrProtocolBase._test_encode(self, params)


StreamZap = StreamZap()
