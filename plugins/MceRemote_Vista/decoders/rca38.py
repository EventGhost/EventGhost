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
from . import rca
from . import protocol_base

TIMING = 460


class RCA38(rca.RCA.__class__):
    """
    IR decoder for the RCA38 protocol.
    """
    irp = '{38.7k,460,msb}<1,-2|1,-4>(8,-8,D:4,F:8,~D:4,~F:8,1,-16)*'
    frequency = 38700

    def _test_decode(self):
        rlc = [[
            3680, -3680, 460, -1840, 460, -1840, 460, -1840, 460, -1840, 460, -1840, 460, -920, 
            460, -920, 460, -920, 460, -1840, 460, -920, 460, -920, 460, -1840, 460, -920, 
            460, -920, 460, -920, 460, -920, 460, -920, 460, -1840, 460, -1840, 460, -1840, 
            460, -920, 460, -1840, 460, -1840, 460, -920, 460, -7360, 
        ]]

        params = [dict(device=15, function=137)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=15, function=137)
        protocol_base.IrProtocolBase._test_encode(self, params)


RCA38 = RCA38()
