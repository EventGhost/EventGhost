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


import eg

class DisplayChoice(eg.Choice):
    """
    A wx.Choice control, that shows all available displays.
    """
    def __init__(self, parent, value, *args, **kwargs):
        choices = list(
            display.number + ': ' + display.name
            for display in eg.DesktopDisplay.displays
        )
        eg.Choice.__init__(self, parent, value, choices, *args, **kwargs)

    def GetStringSelection(self):
        return 'Monitor ' + str(self.GetSelection() + 1)

    def GetDisplaySelection(self):
        return eg.Choice.GetStringSelection(self).split(': ', 1)[1]
