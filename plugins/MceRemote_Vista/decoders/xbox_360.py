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
from . import DecodeError
from . import protocol_base


XBOX360_COMMANDS = {
    0x00: 'Number.0',
    0x01: 'Number.1',
    0x03: 'Number.3',
    0x05: 'Number.5',
    0x07: 'Number.7',
    0x09: 'Number.9',
    0x0C: 'Power.Toggle',
    0x0F: 'Button.Info',
    0x12: 'Channel.Up',
    0x14: 'Media.FastForward',
    0x16: 'Media.Play',
    0x17: 'Media.Record',
    0x18: 'Media.Pause',
    0x1A: 'Media.Next',
    0x1C: 'Button.Reload',
    0x1F: 'Navigation.Down',
    0x20: 'Navigation.Left',
    0x24: 'Menu.DVD',
    0x26: 'Button.Y',
    0x28: 'Button.OpenCloseTray',
    0x4F: 'Button.Display',
    0x66: 'Button.A',
    0x02: 'Number.2',
    0x04: 'Number.4',
    0x06: 'Number.6',
    0x08: 'Number.8',
    0x0A: 'Button.Clear',
    0x0B: 'Navigation.Enter',
    0x0D: 'Button.Start',
    0x0E: 'Volume.Mute',
    0x10: 'Voluem.Down',
    0x11: 'Volume.Up',
    0x13: 'Channel.Down',
    0x15: 'Media.Rewind',
    0x19: 'Media.Toggle',
    0x1B: 'Media.Previous',
    0x1D: 'Button.100',
    0x1E: 'Navigation.Up',
    0x21: 'Navigation.Right',
    0x22: 'Navigation.Ok',
    0x23: 'Navigation.Back',
    0x25: 'Button.B',
    0x51: 'Button.Title',
    0x64: 'Button.Xbox',
    0x68: 'Button.X'
}

OEM1 = 0x80
OEM2 = 0x0F

XBOX1_DEVICE = 0x74

TIMING = 444


class XBox360(protocol_base.IrProtocolBase):
    """
    IR decoder for the RC6632 protocol.
    """
    irp = '{36k,444,msb}<-1,1|1,-1>(6,-2,1:1,6:3,-2,2,OEM1:8,OEM2:8,(1-T):1,D:7,F:8,^107m)*{OEM1=0x80,OEM2=0x0F,D=0x74||0xF4}'
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
        ['function', 0, 255],
        ['toggle', 0, 1]
    ]

    def decode(self, data, frequency=0):
        code = protocol_base.IrProtocolBase.decode(self, data, frequency)

        if code.c0 != 1:
            raise DecodeError('Checksum failed')

        if code.mode != 6:
            raise DecodeError('Incorrect mode')

        if code.oem1 != OEM1 or code.OEM2 != OEM2:
            raise DecodeError('Incorrect oem')

        if code.device != XBOX1_DEVICE:
            raise DecodeError('device is not an XBox360')

        if code.function in XBOX360_COMMANDS:
            code.name = self.__class__.__name__ + '.' + XBOX360_COMMANDS[code.function]

        return code

    def encode(self, function, toggle):
        c0 = 1
        mode = 6
        oem1 = OEM1
        oem2 = OEM2
        device = XBOX1_DEVICE

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

        packets = []
        for function in XBOX360_COMMANDS.keys():
            toggle = 1
            rlc = self.encode(function, toggle)

            params = [dict(function=function, toggle=toggle)]

            packets += [[rlc, params]]

        for rlc, params in packets:
            protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=128, toggle=0, device=85, sub_device=106)
        protocol_base.IrProtocolBase._test_encode(self, params)


XBox360 = XBox360()
