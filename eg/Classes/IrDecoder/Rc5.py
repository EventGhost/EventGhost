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
from eg.Classes.IrDecoder import DecodeError, ManchesterCoding2

ADDRESSES = {
    0x00: "TV1",
    0x01: "TV2",
    0x02: "Teletext",
    0x03: "Video",
    0x04: "LV1",
    0x05: "VCR1",
    0x06: "VCR2",
    0x07: "Experimental",
    0x08: "Sat1",
    0x09: "Camera",
    0x0A: "Sat2",
    0x0B: "0B",
    0x0C: "CD-Video",
    0x0D: "0D",
    0x0E: "CD-Photo",
    0x0F: "0F",
    0x10: "AMP1",
    0x11: "Tuner",
    0x12: "Tape1",
    0x13: "AMP2",
    0x14: "CD",
    0x15: "Phono",
    0x16: "Sat3",
    0x17: "Tape2",
    0x18: "18",
    0x19: "19",
    0x1A: "CD-R",
    0x1B: "1B",
    0x1C: "1C",
    0x1D: "Lightning1",
    0x1E: "Lightning2",
    0x1F: "Phone",
}

CMDS = {
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
    0x0A: "DigitEntry",
    0x0C: "Power",
    0x0D: "Mute",
    0x10: "VolumeUp",
    0x11: "VolumeDown",
    0x12: "BrightnessUp",
    0x13: "BrightnessDown",
    0x20: "ChannelUp",
    0x21: "ChannelDown",
    0x32: "Rewind",
    0x34: "Forward",
    0x35: "Play",
    0x36: "Stop",
    0x37: "Record",
    0x50: "Up",
    0x51: "Down",
    0x52: "Menu",
    0x55: "Left",
    0x56: "Right",
    0x57: "Ok",
    0x6B: "Red",
    0x6C: "Green",
    0x6D: "Yellow",
    0x6E: "Blue",
}

STREAMZAP = {
    0x40: "Num0",
    0x41: "Num1",
    0x42: "Num2",
    0x43: "Num3",
    0x44: "Num4",
    0x45: "Num5",
    0x46: "Num6",
    0x47: "Num7",
    0x48: "Num8",
    0x49: "Num9",
    0x4A: "Power",
    0x4B: "Mute",
    0x4C: "ChannelUp",
    0x4D: "VolumeUp",
    0x4E: "ChannelDown",
    0x4F: "VolumeDown",
    0x50: "Up",
    0x51: "Left",
    0x52: "Ok",
    0x53: "Right",
    0x54: "Down",
    0x55: "Menu",
    0x56: "Exit",
    0x57: "Play",
    0x58: "Pause",
    0x59: "Stop",
    0x5A: "PreviousTrack",
    0x5B: "NextTrack",
    0x5C: "Record",
    0x5D: "Rewind",
    0x5E: "Forward",
    0x60: "Red",
    0x61: "Green",
    0x62: "Yellow",
    0x63: "Blue",
}

class Rc5(ManchesterCoding2):
    """
    IR decoder for the Philips RC-5 protocol.
    """
    lastCode = None
    timeout = 150

    def __init__(self, controller):
        ManchesterCoding2.__init__(self, controller, 889)
        self.lastToggleBit = None

    def Decode(self, data):
        self.SetData(data)
        self.bufferLen = 1
        if not self.GetBit():
            raise DecodeError("missing start bit")
        extensionBit = self.GetBit()
        toggleBit = self.GetBit()
        addr = self.GetBitsLsbLast(5)
        cmd = self.GetBitsLsbLast(6)
        if not extensionBit:
            cmd |= 0x40
        # the Streamzap remote uses a RC-5-like code with an additional command
        # bit
        try:
            streamzapBit = self.GetBit()
        except DecodeError:
            # no additional bit, so this is no Streamzap code
            pass
        else:
            cmd = (cmd << 1) | streamzapBit
            try:
                code = STREAMZAP[cmd]
            except KeyError:
                # eventhough it looks like a Steamzap code, this code is
                # unknown
                raise DecodeError("too many bits")
            return "Streamzap." + code
        cmdStr = CMDS.get(cmd, "%02X" % cmd)
        code = "RC5.%s.%s" % (ADDRESSES[addr], cmdStr)
        if code == self.lastCode and toggleBit != self.lastToggleBit:
            self.lastCode = None
        self.lastToggleBit = toggleBit
        return code
