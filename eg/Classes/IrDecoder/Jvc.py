# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
# 
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from eg.Classes.IrDecoder import IrProtocolBase, DecodeError
from time import clock


class Jvc(IrProtocolBase):
    """
    IR decoder for the JVC protocol.
    """

    def __init__(self, controller):
        IrProtocolBase.__init__(self, controller)
        self.lastTime = clock()


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
        return buf


    def Decode(self, data):
        # Check the header pulse
        pos = 0
        if clock() - self.lastTime > 0.1:
            if not (7400 < data[0] < 9400):
                raise DecodeError("wrong header pulse")
            if not (3200 < data[1] < 5200):
                raise DecodeError("wrong header pause")
            pos = 2
        addr = self.GetByte(data, pos)
        cmd = self.GetByte(data, pos + 16)
        if not (250 < data[pos + 32] < 750):
            raise DecodeError("wrong byte end-pulse")
        if data[pos + 33] < 10000:
            raise DecodeError("missing end-pause")
        self.lastTime = clock()
        return "JVC.%0.2X%0.2X" % (addr, cmd)

