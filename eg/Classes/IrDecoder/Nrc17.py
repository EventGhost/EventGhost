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
                raise DecodeError("pre-space too short %d" % dummyCounter)

        # Check the start bit
        if not self.GetBit():
            raise DecodeError("missing start bit")

        # Get the actual code bits
        code = self.GetBitsLsbFirst(16)
        if code == 0xFFFE:
            return ""
        return "NRC17_%0.4X" % code

