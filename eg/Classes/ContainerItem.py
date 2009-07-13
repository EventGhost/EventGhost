# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg
from TreeItem import TreeItem


class ContainerItem(TreeItem):
    xmlTag = "Container"

    def GetData(self):
        attr, text = TreeItem.GetData(self)
        if self in self.document.expandedNodes:
            attr.append(("Expanded", "True"))
        return attr, text


    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        tagDict = self.document.XMLTag2ClassDict
        self.childs = [
            tagDict[childNode.tag.lower()](self, childNode) 
                for childNode in node
        ]
        if node.attrib.get("expanded", "").lower() == "true":
            self.document.expandedNodes.add(self)


    def Delete(self):
        for child in self.childs[:]:
            child.Delete()
        TreeItem.Delete(self)


    @eg.LogIt
    def AddChild(self, child, pos=-1):
        childs = self.childs
        if pos == -1 or pos >= len(childs):
            childs.append(child)
            pos = -1
        else:
            childs.insert(pos, child)
        eg.Notify("NodeAdded", (child, pos))
        

    def RemoveChild(self, child):
        pos = self.childs.index(child)
        del self.childs[pos]
        eg.Notify("NodeDeleted", child)
        return pos

