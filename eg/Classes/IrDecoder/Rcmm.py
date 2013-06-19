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

from eg.Classes.IrDecoder import IrProtocolBase, DecodeError

MODES = {
    1: "Mouse",
    2: "Keyboard",
    3: "Gamepad",
}

class Rcmm(IrProtocolBase):

    def GetBits(self):
        if 66 > self.data[self.pos] > 266:
            raise DecodeError("wrong pulse")
        pause = self.data[self.pos + 1]
        self.pos += 2
        if pause < 366:
            return 0 # binary 00
        elif pause < 528:
            return 1 # binary 01
        elif pause < 694:
            return 2 # binary 10
        elif pause < 861:
            return 3 # binary 11
        else:
            raise DecodeError("pause to long")


    def ShiftInBits(self, numBits):
        data = 0
        for dummyCounter in xrange(numBits):
            data <<= 2
            data |= self.GetBits()
        return data


    def Decode(self, data):
        raise DecodeError("not implemented")
        if not (200 < data[0] < 600):
            DecodeError("wrong header pulse")
        if not (100 < data[1] < 500):
            DecodeError("wrong header pause")
        self.pos = 2
        self.data = data
        mode = self.GetBits()
        if mode != 0:
            addr = self.GetBits()
            data = self.ShiftInBits(4)
            return "RC-MM.%s.%X.%04X" % (MODES[mode], addr, data)
        mode = self.GetBits()
        if mode != 0:
            data = self.ShiftInBits(10)
            return "RC-MM.Ex%s.%06X" % (MODES[mode], data)
        mode = self.GetBits()
        if mode != 3:
            raise DecodeError("wrong OEM mode")
        customerId = self.ShiftInBits(3)
        data = self.ShiftInBits(6)
        return "RC-MM.Oem%02X.%04X" % (customerId, data)

