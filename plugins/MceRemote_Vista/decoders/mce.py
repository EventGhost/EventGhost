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

MCE_COMMANDS = {
    0x00: "Number.0",
    0x01: "Number.1",
    0x02: "Number.2",
    0x03: "Number.3",
    0x04: "Number.4",
    0x05: "Number.5",
    0x06: "Number.6",
    0x07: "Number.7",
    0x08: "Number.8",
    0x09: "Number.9",
    0x0A: "Navigation.Escape",
    0x0B: "Navigation.Enter",
    0x0C: "Power.Toggle",
    0x0D: "Button.Start",
    0x0E: "Volume.Mute",
    0x0F: "Menu.Info",
    0x10: "Volume.Up",
    0x11: "Volume.Down",
    0x12: "Channel.Up",
    0x13: "Channel.Down",
    0x14: "Media.FastForward",
    0x15: "Media.Rewind",
    0x16: "Media.Play",
    0x17: "Media.Record",
    0x18: "Media.Pause",
    0x19: "Media.Stop",
    0x1A: "Media.Skip",
    0x1B: "Media.Replay",
    0x1C: "Number.Pound",
    0x1D: "Number.Star",
    0x1E: "Navigation.Up",
    0x1F: "Navigation.Down",
    0x20: "Navigation.Left",
    0x21: "Navigation.Right",
    0x22: "Navigation.Ok",
    0x23: "Navigation.Back",
    0x24: "Menu.DVD",
    0x25: "Source.LiveTV",
    0x26: "Menu.Guide",
    0x27: "Video.Aspect",
    0x46: "Source.TV",
    0x47: "Source.Music",
    0x48: "Source.RecordedTV",
    0x49: "Source.Pictures",
    0x4A: "Source.Videos",
    0x4C: "Source.Audio",
    0x4D: "Button.Subtitle",
    0x50: "Source.Radio",
    0x5A: "Button.Teletext",
    0x5B: "Button.Red",
    0x5C: "Button.Green",
    0x5D: "Button.Yellow",
    0x5E: "Button.Blue",
}



OEM1 = 0x80
OEM2 = 0x0F
MCE_DEVICE = 0x04


TIMING = 444


class MCE(protocol_base.IrProtocolBase):
    """
    IR decoder for the RC6632 protocol.
    """
    irp = '{36k,444,msb}<-1,1|1,-1>((6,-2,1:1,6:3,-2,2,OEM1:8,S:8,T:1,D:7,F:8,^107m)*,T=1-T) {OEM1=128}'
    frequency = 36000
    bit_count = 36
    encoding = 'msb'

    _lead_in = [TIMING * 6, -TIMING * 2]
    _lead_out = [107000]
    _middle_timings = [(-TIMING * 2, TIMING * 2)]
    _bursts = [[-TIMING, TIMING], [TIMING, -TIMING]]

    _repeat_lead_in = []
    _repeat_lead_out = []
    _repeat_bursts = []

    _parameters = [
        ['C0', 0, 0],
        ['M', 1, 3],
        ['OEM1', 4, 11],
        ['OEM2', 12, 19],
        ['T', 20, 20],
        ['D', 21, 27],
        ['F', 28, 35],
    ]
    # [D:0..127,S:0..255,F:0..255,T@:0..1=0]
    encode_parameters = [
        ['function', 0, 0x5E],
        ['toggle', 0, 1]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 1 or code.mode != 6 or code.oem1 != OEM1 or code.oem2 != OEM2 or code.device != MCE_DEVICE:
            raise DecodeError('Checksum failed')

        if code.function not in MCE_COMMANDS:
            raise DecodeError('Invalid function')

        code.name = self.__class__.__name__ + '.' + MCE_COMMANDS[code.function]

        return code

    def encode(self, function, toggle):
        c0 = 1
        mode = 6
        oem1 = OEM1
        oem2 = OEM2
        device = MCE_DEVICE
        packet = self._build_packet(
            list(self._get_timing(c0, i) for i in range(1)),
            list(self._get_timing(mode, i) for i in range(3)),
            self._middle_timings[0],
            list(self._get_timing(oem1, i) for i in range(8)),
            list(self._get_timing(oem2, i) for i in range(8)),
            list(self._get_timing(toggle, i) for i in range(1)),
            list(self._get_timing(device, i) for i in range(7)),
            list(self._get_timing(function, i) for i in range(8)),
        )

        return [packet]

    def _test_decode(self):

        for i in range(0x00, 0x5E + 1):
            if (
                0x27 < i < 0x46 or
                0x50 < i < 0x5A or
                i in (0x4B, 0x4E, 0x4F)
            ):
                continue

            rlc = self.encode(i, 1)
            params = [dict(function=i, toggle=1)]

            protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=208, toggle=1)
        protocol_base.IrProtocolBase._test_encode(self, params)


MCE = MCE()

blah = [2664, -888, 444, -444, 444, -444, 444, -888, 444, -888, 1332, -888, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 888, -444, 444, -444, 444, -444, 444, -444, 444, -888, 444, -444, 444, -444, 444, -444, 888, -888, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -69704]
blah = [2664, -888, 444, -444, 444, -444, 444, -888, 444, -888, 1332, -888, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 888, -444, 444, -444, 444, -444, 444, -444, 444, -888, 444, -444, 444, -444, 444, -444, 888, -888, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -444, 444, -69704]





