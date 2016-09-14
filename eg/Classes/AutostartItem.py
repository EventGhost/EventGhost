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
from MacroItem import MacroItem
from TreeItem import HINT_MOVE_INSIDE, HINT_MOVE_AFTER

class AutostartItem(MacroItem):
    xmlTag = "Autostart"
    icon = eg.Icons.AUTOSTART_ICON
    isDeactivatable = False
    isRenameable = False
    isMoveable = False
    dropBehaviour = {
        "Folder": HINT_MOVE_AFTER,
        "Macro": HINT_MOVE_AFTER,
        "Plugin": HINT_MOVE_INSIDE,
        "Action": HINT_MOVE_INSIDE,
    }

    @eg.AssertInActionThread
    def __init__(self, parent, node):
        eg.TreeItem.__init__(self, parent, node)
        tagDict = self.document.XMLTag2ClassDict
        self.childs = []
        for childNode in node:
            childTag = childNode.tag.lower()
            if childTag == "plugin":
                child = self.document.PluginItem(self, childNode)
            else:
                child = None
            self.childs.append(child)
        for i, childNode in enumerate(node):
            childTag = childNode.tag.lower()
            if childTag == "plugin":
                continue
            self.childs[i] = tagDict[childTag](self, childNode)
        if node.attrib.get("expanded", "").lower() == "true":
            self.document.expandedNodes.add(self)
        self.name = eg.text.General.autostartItem
        self.document.autostartMacro = self

    def CanCut(self):
        return False

    def CanCopy(self):
        return False

    def CanDelete(self):
        return False

    def Enable(self, flag=True):
        # never disable the Autostart item
        pass

    @eg.LogIt
    @eg.AssertInActionThread
    def UnloadPlugins(self):
        for child in self.childs:
            if child.__class__ == self.document.PluginItem:
                child.info.Close()
                child.info.RemovePluginInstance()
