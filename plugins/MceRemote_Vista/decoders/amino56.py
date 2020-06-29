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
from . import amino
from . import protocol_base


class Amino56(amino.Amino.__class__):
    """
    IR decoder for the Amino56 protocol.
    """
    irp = (
        '{56.0k,268,msb}<-1,1|1,-1>([T=1][T=0],7,-6,3,D:4,1:1,T:1,1:2,0:8,F:8,15:4,C:4,-79m)+'
        '{C=(D:4+4*T+9+F:4+F:4:4+15)&15}'
    )
    frequency = 56000

    def _test_decode(self):
        rlc = [[
            1876, -1608, 804, -268, 536, -268, 268, -268, 268, -268, 268, -268, 268, -536, 536, -536, 268, -268,
            268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -268, 536, -268, 268, -268, 268, -268,
            268, -268, 268, -536, 268, -268, 536, -268, 268, -268, 268, -268, 268, -268, 268, -268, 268, -536,
            536, -268, 268, -79268
        ]]

        params = [dict(device=7, function=249)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=7, function=249)
        protocol_base.IrProtocolBase._test_encode(self, params)


Amino56 = Amino56()
