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
from eg.Classes.IrDecoder import DecodeError, ManchesterCoding1

MCE_REMOTE = {
    0x800F0400: "Num0",
    0x800F0401: "Num1",
    0x800F0402: "Num2",
    0x800F0403: "Num3",
    0x800F0404: "Num4",
    0x800F0405: "Num5",
    0x800F0406: "Num6",
    0x800F0407: "Num7",
    0x800F0408: "Num8",
    0x800F0409: "Num9",
    0x800F040A: "Escape",
    0x800F040B: "Enter",
    0x800F040C: "Power",
    0x800F040D: "Start",
    0x800F040E: "Mute",
    0x800F040F: "Details",
    0x800F0410: "VolumeUp",
    0x800F0411: "VolumeDown",
    0x800F0412: "ChannelUp",
    0x800F0413: "ChannelDown",
    0x800F0414: "Forward",
    0x800F0415: "Rewind",
    0x800F0416: "Play",
    0x800F0417: "Record",
    0x800F0418: "Pause",
    0x800F0419: "Stop",
    0x800F041A: "Skip",
    0x800F041B: "Replay",
    0x800F041C: "Pound",
    0x800F041D: "Star",
    0x800F041E: "Up",
    0x800F041F: "Down",
    0x800F0420: "Left",
    0x800F0421: "Right",
    0x800F0422: "Ok",
    0x800F0423: "Back",
    0x800F0424: "DVDMenu",
    0x800F0425: "LiveTV",
    0x800F0426: "Guide",
    0x800F0427: "Aspect",
    0x800F0446: "TV",
    0x800F0447: "Music",
    0x800F0448: "Recorded_TV",
    0x800F0449: "Pictures",
    0x800F044A: "Videos",
    0x800F044C: "Audio",
    0x800F044D: "Subtitle",
    0x800F0450: "Radio",
    0x800F045A: "Teletext",
    0x800F045B: "Red",
    0x800F045C: "Green",
    0x800F045D: "Yellow",
    0x800F045E: "Blue",
}

class Rc6(ManchesterCoding1):
    """
    IR decoder for the Philips RC-6 protocol.
    """
    timeout = 150

    def __init__(self, controller):
        ManchesterCoding1.__init__(self, controller, 444)

    def Decode(self, data):
        # Check the leader pulse
        if not (2200 < data[0] < 3300):
            raise DecodeError("wrong header pulse")
        if not (600 < data[1] < 1100):
            raise DecodeError("wrong header pause")

        self.SetData(data, 2)

        # Get the start bit
        if self.GetBit() != 1:
            raise DecodeError("missing start bit")

        mode = self.GetBitsLsbLast(3)
        trailerBit = self.GetTrailerBit()
        value = self.GetBitsLsbLast(32)

        # Check for MCE remote
        if mode == 6 and trailerBit == 0:
            value2 = value & 0xFFFF7FFF
            if value2 in MCE_REMOTE:
                return "Mce." + MCE_REMOTE[value2]
#            else:
#                print "0x%0.8X" % value2

        return "RC6mode%X_%d_%08X" % (mode, trailerBit, value)

    def GetTrailerBit(self):
        sample = (
            self.GetSample() * 8 +
            self.GetSample() * 4 +
            self.GetSample() * 2 +
            self.GetSample()
        )
        if sample == 3:  # binary 0011
            return 0
        elif sample == 12:  # binary 1100
            return 1
        else:
            raise DecodeError("wrong trailer bit transition")
