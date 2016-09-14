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

# Local imports
from RadioButtonGrid import RadioButtonGrid

class CheckBoxGrid(RadioButtonGrid):
    CtrlType = wx.CheckBox

    def GetValue(self):
        result = []
        for column in self.ctrlTable:
            value = 0
            for i, ctrl in enumerate(column):
                if ctrl.GetValue():
                    value |= (1 << i)
            result.append(value)
        return result

    def SetValue(self, value):
        for x, val in enumerate(value):
            column = self.ctrlTable[x]
            for i, ctrl in enumerate(column):
                ctrl.SetValue(val & (1 << i))
