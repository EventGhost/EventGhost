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
import eg
from ContainerItem import ContainerItem
from TreeItem import HINT_MOVE_INSIDE, HINT_MOVE_BEFORE_OR_AFTER

class MacroItem(ContainerItem):
    xmlTag = "Macro"
    icon = eg.Icons.MACRO_ICON
    isExecutable = True
    shouldSelectOnExecute = False
    dropBehaviour = {
        "Event": HINT_MOVE_INSIDE,
        "Macro": HINT_MOVE_BEFORE_OR_AFTER,
        "Folder": HINT_MOVE_BEFORE_OR_AFTER,
        "Action": HINT_MOVE_INSIDE,
    }

    def Execute(self):
        if self.isEnabled:
            del eg.lastFoundWindows[:]
            if eg.config.logMacros:
                self.Print(self.name)
            if self.shouldSelectOnExecute:
                wx.CallAfter(self.Select)

            if self.childs:
                eg.indent += 1
                eg.programCounter = (self.childs[0], 0)
            else:
                eg.programCounter = None

    def GetNextChild(self, index):
        index += 1
        if len(self.childs) > index:
            return self.childs[index], index
        else:
            return None
