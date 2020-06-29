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
from . import nrc16


class NRC1632(nrc16.NRC16.__class__):
    """
    IR decoder for the NRC1632 protocol.
    """
    irp = '{32k,500,lsb}<-1,1|1,-1>(1,-5,1:1,254:8,127:7,-15m,(1,-5,1:1,F:8,D:7,-110m)+,1,-5,1:1,254:8,127:7,-15m)'
    frequency = 32000


NRC1632 = NRC1632()
