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


class Sony(IrProtocolBase):
    """
    IR decoder for the Sony SIRC protocol.
    """

    def Decode(self, data):
        if not (1800 < data[0] < 3000):
            raise DecodeError("wrong header pulse")

        buf = 0
        mask = 1
        i = 1
        while True:
            # Check if the space time is valid.
            space = data[i]
            if space < 400:
                raise DecodeError("space to short %d" % space)
            if space > 900:
                if i in (25, 31, 41):
                    break
                raise DecodeError("space to long %d" % space)

            mark = data[i+1]
            if mark < 250:
                raise DecodeError("mark to short %d" % mark)
            elif mark < 1000:
                pass
            elif mark < 1400:
                buf |= mask
            else:
                raise DecodeError("mark to long %d" % mark)
            mask <<= 1
            i += 2

        return "SIRC%d.%0.4X" % (i / 2, buf)

