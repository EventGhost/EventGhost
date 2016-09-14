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

from time import clock

# Local imports
from eg.Classes.IrDecoder import DecodeError, IrProtocolBase

class Nec(IrProtocolBase):
    """
    IR decoder for the NEC protocol.
    """
    timeout = 150

    def __init__(self, controller):
        IrProtocolBase.__init__(self, controller)
        self.lastTime = 0

    def Decode(self, data):
        pulse = data[0]
        space = data[1]
        if not (8000 < pulse < 10000):
            raise DecodeError("wrong start pulse")
        if space > 5000:
            raise DecodeError("start pause too long")
        if space < 4000:
            if space > 2000 and self.lastTime + 0.150 > clock():
                #print "repeat", clock() - self.lastTime, self.lastCode
                self.lastTime = clock()
                return self.lastCode
            raise DecodeError("wrong start pause")
        buf = 0
        for i in range(2, 62, 2):
            pulse = data[i]
            if pulse > 750:
                raise DecodeError("mark too long %d %d" % (pulse, i))
            if pulse < 450:
                raise DecodeError("mark too short")
            space = data[i + 1]
            if space < 350:
                raise DecodeError("space too short %d %d" % (space, i + 1))
            elif space < 850:
                pass
            elif space < 2000:
                buf |= 1
            else:
                raise DecodeError("space too long %d" % space)
            buf <<= 1
        self.lastTime = clock()
        return "NEC.%08X" % buf
