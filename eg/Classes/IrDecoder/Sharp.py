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

SHARP_TIME = 0.000320  # 320 micro-seconds


class Sharp(IrProtocolBase):
    """
    IR decoder for the Sharp/Denon protocol.
    """
    timeout = 120

    def Decode(self, data):
        buf = 0
        for i in range(16):
            mark = data[i*2]
            if mark < 100:
                raise DecodeError("mark too short")
            if mark > 500:
                raise DecodeError("mark too long")
            space = data[i*2+1]
            if space < 600:
                raise DecodeError("space too short")
            elif space < 1200:
                pass
            elif space < 2100:
                buf |= 1
            else:
                if i == 15:
                    break
                raise DecodeError("space too long")
            buf <<= 1
        else:
            raise DecodeError("sequence too long")
        buf >>= 1
        if (buf & 256):
            buf ^= 0x03ff
        return "Sharp.%0.4X" % (buf)

