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
from . import arctech
from . import protocol_base


class Arctech38(arctech.Arctech.__class__):
    """
    IR decoder for the Arctech38 protocol.
    """
    irp = '{38k,388,lsb}<1,-3|3,-1>(<0:2|2:2>((D-1):4,(S-1):4),40:7,F:1,0:1,-10.2m)*'
    frequency = 38000

    def _test_decode(self):
        return
        rlc = [
            388, -1164, 388, -1164, 388, -1164, 1164, -388, 388, -1164, 1164, -388, 388, -1164,
            1164, -388, 388, -1164, 1164, -388, 388, -1164, 388, -1164, 388, -1164, 1164, -388,
            388, -1164, 388, -1164, 388, -1164, 388, -1164, 388, -1164, 1164, -388, 388, -1164,
            1164, -388, 388, -1164, 1164, -388, 388, -11364,
        ]

        params = dict(device=15, function=1, sub_device=6)

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        return
        params = dict(device=15, function=1, sub_device=6)
        protocol_base.IrProtocolBase._test_encode(self, params)




Arctech38 = Arctech38()
