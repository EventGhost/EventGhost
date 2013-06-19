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

from eg.Classes.IrDecoder import ManchesterCoding1, DecodeError


class Nrc17(ManchesterCoding1):
    """
    IR decoder for the Nokia NRC17 protocol.
    """

    def __init__(self, controller):
        ManchesterCoding1.__init__(self, controller, 500)


    def Decode(self, data):
        self.SetData(data)
        # Consume the pre-pulse bit
        self.GetSample()

        # Check the header pause
        for dummyCounter in range(5):
            if self.GetSample():
                raise DecodeError("pre-space to short %d" % dummyCounter)

        # Check the start bit
        if not self.GetBit():
            raise DecodeError("missing start bit")

        # Get the actual code bits
        code = self.GetBitsLsbFirst(16)
        if code == 0xFFFE:
            return ""
        return "NRC17_%0.4X" % code

