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
from . import protocol_base
from . import rc57f


class RC57F57(rc57f.RC57F.__class__):
    """
    IR decoder for the RC57F57 protocol.
    """
    irp = '{57k,889,msb}<1,-1|-1,1>(1,~D:1:5,T:1,D:5,F:7,^114m)*'
    frequency = 57000

    def _test_decode(self):
        rlc = [[
            889, -889, 1778, -889, 889, -1778, 889, -889, 1778, -889, 889, -889, 889, -1778,
            1778, -889, 889, -889, 889, -889, 889, -1778, 889, -88219,
        ]]

        params = [dict(function=33, toggle=0, device=12)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)

    def _test_encode(self):
        params = dict(function=33, toggle=0, device=12)
        protocol_base.IrProtocolBase._test_encode(self, params)


RC57F57 = RC57F57()
