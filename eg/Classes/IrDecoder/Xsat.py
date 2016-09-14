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
from eg.Classes.IrDecoder import DecodeError, IrProtocolBase

class Xsat(IrProtocolBase):
    """
    IR decoder for the X-Sat protocol.
    """
    def Decode(self, data):
        # Check the header pulse
        if not (7000 < data[0] < 9000):
            raise DecodeError("wrong header pulse")
        if not (3000 < data[1] < 5000):
            raise DecodeError("wrong header pause")
        if not (3000 < data[19] < 5000):
            raise DecodeError("wrong middle pause")

        addr = self.GetByte(data, 2)
        cmd = self.GetByte(data, 20)
        if data[37] < 10000:
            raise DecodeError("sequence too long")
        return "XSAT.%0.2X%0.2X" % (addr, cmd)

    def GetByte(self, data, pos):
        buf = 0
        mask = 1
        for i in range(8):
            pulse = data[pos]
            pos += 1
            if not (250 < pulse < 750):
                raise DecodeError("wrong pulse %d %d" % (pulse, i))
            space = data[pos]
            pos += 1
            if space < 250:
                raise DecodeError("space to short %d %d" % (space, i))
            elif space < 850:
                pass
            elif space < 1800:
                buf |= mask
            else:
                raise DecodeError("space too long")
            mask <<= 1
        pulse = data[pos]
        if 250 > pulse > 750:
            raise DecodeError("wrong byte end-pulse")
        return buf
