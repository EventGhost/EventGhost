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
from . import proton
from . import protocol_base


TIMING = 500


class Proton40(proton.Proton.__class__):
    """
    IR decoder for the Proton40 protocol.
    """
    irp = '{40.5k,500,lsb}<1,-1|1,-3>(16,-8,D:8,1,-8,F:8,1,^63m)*'
    frequency = 40500

    def _test_decode(self):
        rlc = [[
            8000, -4000, 500, -500, 500, -500, 500, -1500, 500, -1500, 500, -1500, 500, -500,
            500, -1500, 500, -1500, 500, -4000, 500, -1500, 500, -500, 500, -500, 500, -1500,
            500, -1500, 500, -500, 500, -500, 500, -1500, 500, -21000,
        ]]

        params = [dict(device=220, function=153)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(device=220, function=153)
        protocol_base.IrProtocolBase._test_encode(self, params)


Proton40 = Proton40()
