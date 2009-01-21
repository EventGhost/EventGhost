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
# $LastChangedDate: 2008-12-29 19:13:21 +0100 (Mo, 29 Dez 2008) $
# $LastChangedRevision: 649 $
# $LastChangedBy: bitmonster $

from eg.Classes.IrDecoder import DecodeError


MCE_REMOTE = {
    0x800F0420: "Left",
    0x800F0421: "Right",
    0x800F0422: "Ok",
    0x800F041E: "Up",
    0x800F041F: "Down",
    0x800F0423: "Back",
    0x800F0410: "VolumeUp",
    0x800F0411: "VolumeDown",
    0x800F0412: "ChannelUp",
    0x800F0413: "ChannelDown",
    0x800F040E: "Mute",
    0x800F040D: "Start",
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
    0x800F045A: "Teletext",
    0x800F045B: "Red",
    0x800F045C: "Green",
    0x800F045D: "Yellow",
    0x800F045E: "Blue",
    0x800F040A: "Escape",
    0x800F040B: "Enter",
    0x800F040C: "Power",
    0x800F0416: "Play",
    0x800F0417: "Record",
    0x800F0418: "Pause",
    0x800F0419: "Stop",
    0x800F041A: "Skip",
    0x800F041B: "Replay",
    0x800F0426: "Guide",
    0x800F0448: "Recorded_TV",
    0x800F040F: "Details",
    0x800F0425: "LiveTV",
    0x800F0424: "DVDMenu",
    0x800F0414: "Forward",
    0x800F0415: "Rewind",
    0x800F0446: "TV",
    0x800F0447: "Music",
    0x800F0449: "Pictures",
    0x800F044A: "Videos",
    0x800F041D: "Star",
    0x800F041C: "Pound",
}


class Rc6Decoder(object):
    
    def __init__(self):
        self.pos = 0
        self.bufferLen = 0
        self.buffer = 0
        self.data = None
        
        
    def GetSample(self):
        if self.bufferLen == 0:
            if self.pos >= len(self.data):
                raise DecodeError
            x = self.data[self.pos]
            self.pos += 1
            bit = self.pos % 2
            if x < 300:
                raise DecodeError
            elif x < 600:
                return bit
            elif x < 1100:
                self.bufferLen = 1
            elif x < 1600:
                self.bufferLen = 2
#            else:
#                raise DecodeError
            self.buffer = bit
            return bit
        self.bufferLen -= 1
        return self.buffer

            
        
    def GetBit(self):
        sample = self.GetSample() * 2 + self.GetSample()
        if sample == 1: # binary 01
            return 0
        elif sample == 2: # binary 10
            return 1
        else:
            raise DecodeError
        
    
    def GetTrailerBit(self):
        sample = (
            self.GetSample() * 8 
            + self.GetSample() * 4 
            + self.GetSample() * 2 
            + self.GetSample()
        )
        if sample == 3: # binary 0011
            return 0
        elif sample == 12: # binary 1100
            return 1
        else:
            raise DecodeError
        
    
    def Decode(self, data):
        self.data = data
        
        # header pulse
        if not (2200 < data[0] < 3300):
            raise DecodeError
        if not (700 < data[1] < 1000):
            raise DecodeError
        self.pos = 2
        
        self.buffer = 0x00
        self.bufferLen = 0
        
        # start bit
        if self.GetBit() != 1:
            raise DecodeError
        
        # mode bits
        mode = 0
        for dummyCounter in range(3):
            mode <<= 1
            if self.GetBit() == 1:
                mode += 1
        
        # trailer bit
        trailerBit = self.GetTrailerBit()
        
        # value bits
        value = 0
        for dummyCounter in range(32):
            value <<= 1
            if self.GetBit() == 1:
                value += 1
        if mode == 6 and trailerBit == 0:
            #value &= 0x7FFF
            value &= 0xFFFF7FFF
            if value in MCE_REMOTE:
                return MCE_REMOTE[value]
#            else:
#                print "0x%0.8X" % value

        return "RC6mode%X_%d_%08X" % (mode, trailerBit, value)
