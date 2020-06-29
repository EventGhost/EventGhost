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
from . import recs800045
from . import protocol_base

TIMING = 158


class RECS800090(recs800045.RECS800045.__class__):
    """
    IR decoder for the RECS800068 protocol.
    """
    irp = '{0k,158,msb}<1,-31|1,-47>(1:1,T:1,D:3,F:6,1,^138m)*'
    frequency = 0

    _lead_out = [TIMING, 138000]
    _bursts = [[TIMING, -TIMING * 31], [TIMING, -TIMING * 47]]

    def _test_decode(self):
        rlc = [[
            +158, -7426, +158, -4898, +158, -7426, +158, -4898, +158, -7426, +158, -7426, +158, -7426, +158, -7426,
            +158, -4898, +158, -4898, +158, -7426, +158, -64530
        ]]

        params = [dict(function=57, toggle=0, device=5)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)


RECS800090 = RECS800090()
