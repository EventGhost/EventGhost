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


class Zaptor56(protocol_base.IRPNotation):
    """
    IR decoder for the Zaptor56 protocol.
    """
    irp = '{56k,330,msb}<-1,1|1,-1>(8,-6,2,D:8,T:1,S:7,F:8,E:4,(((D:4)+(D:4:4)+(S:4)+(S:3:4)+(8*T)+(F:4)+(F:4:4)+E)&15):4,-74m)'


Zaptor56 = Zaptor56()
