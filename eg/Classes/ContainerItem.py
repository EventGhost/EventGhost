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
from TreeItem import TreeItem

class ContainerItem(TreeItem):
    xmlTag = "Container"

    @eg.AssertInActionThread
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        tagDict = self.document.XMLTag2ClassDict
        self.childs = [
            tagDict[childNode.tag.lower()](self, childNode)
            for childNode in node
        ]
        if node.attrib.get("expanded", "").lower() == "true":
            self.document.expandedNodes.add(self)

    @eg.AssertInActionThread
    @eg.LogIt
    def AddChild(self, child, pos=-1):
        childs = self.childs
        if pos == -1 or pos >= len(childs):
            childs.append(child)
            pos = -1
        else:
            childs.insert(pos, child)
        wx.CallAfter(eg.Notify, "NodeAdded", (child, pos))

    @eg.AssertInActionThread
    def Delete(self):
        for child in self.childs[:]:
            child.Delete()
        TreeItem.Delete(self)

    def GetData(self):
        attr, text = TreeItem.GetData(self)
        if self in self.document.expandedNodes:
            attr.append(("Expanded", "True"))
        return attr, text

    @eg.AssertInActionThread
    def RemoveChild(self, child):
        pos = self.childs.index(child)
        del self.childs[pos]
        wx.CallAfter(eg.Notify, "NodeDeleted", (child, self))
        return pos
