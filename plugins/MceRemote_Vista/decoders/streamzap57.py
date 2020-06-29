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
from . import streamzap


class StreamZap57(streamzap.StreamZap.__class__):
    """
    IR decoder for the StreamZap57 protocol.
    """
    irp = '{57k,889,msb}<1,-1|-1,1>(1,~F:1:6,T:1,D:6,F:6,^114m)*'
    frequency = 57000


StreamZap57 = StreamZap57()
