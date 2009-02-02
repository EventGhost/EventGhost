# This file is part of EventGhost.
# Copyright (C) 2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from eg.Classes.IrDecoder import ManchesterCoding2, DecodeError


ADDRESSES = {
    0: "TV1",
    1: "TV2",
    2: "Teletext",
    3: "Video",
    4: "LV1",
    5: "VCR1",
    6: "VCR2",
    7: "Experimental",
    8: "Sat1",
    9: "Camera",
    10: "Sat2",
    11: "0B",
    12: "CD-Video",
    13: "0D",
    14: "CD-Photo",
    15: "0F",
    16: "AMP1",
    17: "Tuner",
    18: "Tape1",
    19: "AMP2",
    20: "CD",
    21: "Phono",
    22: "Sat3",
    23: "Tape2",
    24: "18",
    25: "19",
    26: "CD-R",
    27: "1B",
    28: "1C",
    29: "Lightning1",
    30: "Lightning2",
    31: "Phone",
}

CMDS = {
    0: "Num0",
    1: "Num1",
    2: "Num2",
    3: "Num3",
    4: "Num4",
    5: "Num5",
    6: "Num6",
    7: "Num7",
    8: "Num8",
    9: "Num9",
    0x0A: "DigitEntry",
    0x0C: "Power",
    0x0D: "Mute",
    16: "VolumeUp",
    17: "VolumeDown",
    18: "BrightnessUp",
    19: "BrightnessDown",
    32: "ChannelUp",
    33: "ChannelDown",
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
                raise DecodeError("to many bits")
            return "Streamzap." + code
        cmdStr = CMDS.get(cmd, "%02X" % cmd)
        code = "RC5.%s.%s" % (ADDRESSES[addr], cmdStr)
        if code == self.lastCode and toggleBit != self.lastToggleBit:
            self.lastCode = None
        self.lastToggleBit = toggleBit
        return code
            
            
