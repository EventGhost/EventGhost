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

class Motorola(ManchesterCoding1):
    def __init__(self, controller):
        ManchesterCoding1.__init__(self, controller, 500)

    def Decode(self, data):
        # Check the header pulse
        if not (300 < data[0] < 700):
            raise DecodeError("wrong header pulse")
        if not (2000 < data[1] < 3000):
            raise DecodeError("wrong header pause")
        #print data
        self.SetData(data, 2)
        mask = 1
        buf = 0
        for i in range(20):
            try:
                buf |= mask * self.GetBit()
            except DecodeError:
                if i < 7:
                    raise
                break
            mask <<= 1

        #if data[self.pos] < 10000:
        #    raise DecodeError("missing end pause")
#        if buf == 0x7D:
#            return ""
        return "Motorola%d.%04X" % (i, buf >> 1)
