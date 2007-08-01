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

import wx
import eg
from TreeItem import TreeItem



class ContainerItem(TreeItem):
    xmlTag = "Container"
    
    def WriteToXML(self):
        attr, text, childs = TreeItem.WriteToXML(self)
        if self.isExpanded:
            attr.append(("Expanded", "True"))
        return attr, text, childs
    
    
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        self.childs = []
        for childNode in node:
            cls = self.document.XMLTag2ClassDict[childNode.tag]
            child = cls(self, childNode)
            self.childs.append(child)
        self.isExpanded = node.attrib.get("expanded") == "True"
        
            
    @eg.AssertNotMainThread
    def CreateTreeItem(self, tree, parentId):
        id = TreeItem.CreateTreeItem(self, tree, parentId)
        if len(self.childs):
            tree.SetItemHasChildren(id, True)
            if self.isExpanded:
                tree.Expand(self.id)
        return id
            
        
    @eg.AssertNotMainThread
    def CreateTreeItemAt(self, tree, parentId, pos):
        id = TreeItem.CreateTreeItemAt(self, tree, parentId, pos)
        if len(self.childs):
            tree.SetItemHasChildren(id, True)
            if self.isExpanded:
                tree.Expand(self.id)
        return id

    
    def _Delete(self):
        for child in self.childs[:]:
            child._Delete()
        TreeItem._Delete(self)
        
        
    @eg.AssertNotMainThread
    @eg.LogIt
    def AddChild(self, child, pos=-1):
        childs = self.childs
        tree = self.tree
        isValidId = self.HasValidId()
        id = self.id
        if len(childs) == 0 and isValidId:
            tree.SetItemHasChildren(id)
        if pos == -1 or pos >= len(childs):
            childs.append(child)
            pos = -1
        else:
            childs.insert(pos, child)
        if isValidId and (id == self.root.id or tree.IsExpanded(id)):
            child.CreateTreeItemAt(tree, id, pos)
            
            
    @eg.AssertNotMainThread
    def RemoveChild(self, child):
        pos = self.childs.index(child)
        del self.childs[pos]
        tree = self.tree
        if child.HasValidId():
            tree.Delete(child.id)
        if len(self.childs) == 0 and self.HasValidId():
            tree.SetItemHasChildren(self.id, False)
        return pos
            
        
