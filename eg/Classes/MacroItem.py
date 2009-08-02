# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
# 
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx
from ContainerItem import ContainerItem
from TreeItem import HINT_NO_DROP, HINT_MOVE_INSIDE, HINT_MOVE_BEFORE_OR_AFTER


class MacroItem(ContainerItem):
    xmlTag = "Macro"
    icon = eg.Icons.MACRO_ICON
    isExecutable = True
    shouldSelectOnExecute = False


    def GetNextChild(self, index):
        index += 1
        if len(self.childs) > index:
            return self.childs[index], index
        else:
            return None


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


    def DropTest(self, cls):
        if cls == eg.EventItem:
            return HINT_MOVE_INSIDE
        if cls == eg.MacroItem:
            return HINT_MOVE_BEFORE_OR_AFTER
        if cls == eg.FolderItem:
            return HINT_MOVE_BEFORE_OR_AFTER
        if cls == eg.ActionItem:
            return HINT_MOVE_INSIDE
        return HINT_NO_DROP

