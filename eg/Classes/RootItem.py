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
import wx
import time
from ContainerItem import ContainerItem
from TreeItem import HINT_NO_DROP, HINT_MOVE_INSIDE


class RootItem(ContainerItem):
    xmlTag = "EventGhost"    
    icon = eg.Icons.PathIcon("images/root.png")
    time = None
    guid = None
    isDeactivatable = False
    isRenameable = False            
    
    def GetData(self):
        from comtypes import GUID
        attr, text = ContainerItem.GetData(self)
        self.guid = str(GUID.create_new())
        self.time = str(time.time())
        attr.append(('Version', str(eg.revision)))
        attr.append(('Guid', self.guid))
        attr.append(('Time', self.time))
        return attr, text


    def __init__(self, parent, node):
        parent = None
        ContainerItem.__init__(self, parent, node)
        self.guid = node.attrib.get("guid", "0")
        self.time = node.attrib.get("time", "0")
        self.name = eg.text.General.configTree
         
        
    def CreateTreeItem(self, tree, parentId):
        self.id = tree.AddRoot(
            self.name,
            self.icon.index, 
            -1, 
            wx.TreeItemData(self)
        )
        item = tree.AppendItem(self.id, '')
        font1 = tree.GetItemFont(self.id)
        tree.normalfont = font1
        tree.Delete(item)
        item = tree.AppendItem(self.id, 'a')
        tree.SetItemHasChildren(self.id, True)
        # evil workaround to get another font
        font2 = tree.GetItemFont(item)
        font2.SetStyle(wx.FONTSTYLE_ITALIC)
        tree.Delete(item)
        tree.italicfont = font2
        #for child in self.childs:
        #    child.CreateTreeItem(tree, self.id)
        return id


    def _Delete(self):
        childs = self.childs[:]
        for child in childs:
            child._Delete()


    #@eg.AssertNotMainThread
    def Select(self):
        if self.tree:
            self.tree.SelectItem(self.id)

    
    def EnsureValidId(self, tree):
        pass
            
            
    def CanCut(self):
        return False
    
    
    def CanCopy(self):
        return False
    
    
    def CanDelete(self):
        return False
    
    
    def Enable(self, flag=True):
        pass
    
    
    def DropTest(self, cls):
        if cls == eg.MacroItem:
            return HINT_MOVE_INSIDE
        if cls == eg.FolderItem:
            return HINT_MOVE_INSIDE
        return HINT_NO_DROP
    
