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

import wx

class Choice(wx.Choice):
    def __init__(
        self,
        parent,
        value,
        choices,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        *args,
        **kwargs
    ):
        wx.Choice.__init__(
            self, parent, -1, pos, size, choices, *args, **kwargs
        )
        self.SetValue(value)

    def GetValue(self):
        return self.GetSelection()

    def SetValue(self, value):
        self.SetSelection(value)
