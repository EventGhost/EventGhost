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
from . import dyson
from . import protocol_base

TIMING = 780


class Dyson2(dyson.Dyson.__class__):
    """
    IR decoder for the Dyson2 protocol.
    """
    irp = '{38k,780,lsb}<1,-1|1,-2>(3,-1,D:7,F:6,T:-2,1,-400m,3,-1,D:7,F:6,T:-2,1,-60m,(3,-1,1:1,1,-60m)*)'

    _middle_timings = [(TIMING, -400000), (TIMING * 3, -TIMING)]

    def _test_decode(self):
        rlc = [[
            2340, -780, 780, -1560, 780, -780, 780, -780, 780, -1560, 780, -780, 780, -780,
            780, -1560, 780, -780, 780, -1560, 780, -780, 780, -780, 780, -1560, 780, -780,
            780, -780, 780, -780, 780, -400000, 2340, -780, 780, -1560, 780, -780, 780, -780,
            780, -1560, 780, -780, 780, -780, 780, -1560, 780, -780, 780, -1560, 780, -780,
            780, -780, 780, -1560, 780, -780, 780, -780, 780, -780, 780, -60000,
        ]]

        params = [dict(function=18, toggle=0, device=73)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=18, toggle=0, device=73)
        protocol_base.IrProtocolBase._test_encode(self, params)


Dyson2 = Dyson2()
