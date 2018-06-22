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
import eg


class EventGhostEnduringEvent(eg.EventGhostEvent):
    icon = eg.Icons.ENDURING_EVENT_ICON

    def __init__(self, suffix="", payload=None, prefix="Main", source=eg):
        eventString = prefix + "." + suffix

        if eventString in eg.eventTable:
            for item in eg.eventTable[eventString]:
                if item.icon == eg.Icons.EVENT_ICON:
                    item.icon = eg.Icons.ENDURING_EVENT_ICON
                    item.Refresh()

        eg.EventGhostEvent.__init__(self, suffix, payload, prefix, source)
