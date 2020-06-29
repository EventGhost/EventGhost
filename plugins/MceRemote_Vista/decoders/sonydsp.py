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


class SonyDSP(protocol_base.IRPNotation):
    """
    IR decoder for the SonyDSP protocol.
    """
    irp = '{40k,600}<1,-1|2,-1>((4,-1,96:8,18:7,^45m)3,(4,-1,195:8,^45m),(4,-1,81:8,^45m),(4,-1,F:8,^45m),(4,-1,(F^145):8,11:7,^45m))'


SonyDSP = SonyDSP()
