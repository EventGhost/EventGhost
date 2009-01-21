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

SHARP_TIME = 0.000320  # 320 micro-seconds


def DigitList(value, numdigits=8, base=2):
    val = value
    digits = [0 for i in range(numdigits)]
    for i in range(numdigits):
        val, digits[i] = divmod(val, base)
    digits.reverse()
    return "".join(chr(x+48) for x in digits)



class SharpDecoder(object):
    
    def Decode(self, data):
        buf = 0
        mask = 1
        for i in range(16):
            mark = data[i*2]
            if mark < 200:
                return
            if mark > 500:
                return None
            space = data[i*2+1]
            if space < 600:
                print "space to short", space
                return None
            elif space < 1200:
                pass
            elif space < 2100:
                buf |= mask
            else:
                if i == 15:
                    break
                print "space to long", space, i
                return None
            mask <<= 1
        else:
            return None
        addr = buf & 0x1F
        command = (buf >> 5) & 0xFF
        print DigitList(buf, 16)
#        if (buf & 256):
#            command ^= 0x03ff
        return "Sharp_%0.4X" % ((buf>>5) & 0xFF)
