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
import wx.gizmos

eg.RegisterPlugin(
    name = "System Tray Menu",
    description = (
        "Allows you to add custom menu entries to the tray menu of EventGhost."
    ),
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
)


class Text:
    labelHeader = "Label"
    eventHeader = "Event"
    editLabel = "Label:"
    editEvent = "Event:"
    addBox = "Append:"
    addItemButton = "Menu Item"
    addSeparatorButton = "Separator"
    deleteButton = "Delete"
    unnamedLabel = "New Menu Item %s"
    unnamedEvent = "Event%s"
    
    
    
class TreeListCtrl(wx.gizmos.TreeListCtrl):
    
    def __init__(self, *args, **kwargs):
        wx.gizmos.TreeListCtrl.__init__(self, *args, **kwargs)
        self.__inSizing = False
        self.GetMainWindow().Bind(wx.EVT_SIZE, self.OnSize)
        
    
    def OnSize(self, event):
        event.Skip()
        if not self.__inSizing:
            self.__inSizing = True
            wx.CallAfter(self.OnSize2)
        
        
    def OnSize2(self):
        w, h = self.GetMainWindow().GetClientSize()
        self.SetColumnWidth(1, w - self.GetColumnWidth(0))
        self.__inSizing = False
        
        
    def GetPrevious(self, item):
        previous = self.GetPrevSibling(item)
        if previous.IsOk():
            return previous
        previous = self.GetItemParent(item)
        if not self.HasChildren(previous):
            return previous
        return self.GetLastChild(previous)[0]
    
    
    def GetNext(self, item):
        if self.HasChildren(item):
            return self.GetFirstChild()
        while 1:
            next = self.GetNextSibling(item)
            if next.IsOk():
                return next
            item = self.GetItemParent(item)
            if item == self.GetRootItem():
                return None
        
        
    def CopyItem(self, item, parent, prev=None):
        text = self.GetItemText(item)
        img = self.GetItemImage(item, wx.TreeItemIcon_Normal)
        selImg = self.GetItemImage(item, wx.TreeItemIcon_Selected)
        data = self.GetPyData(item)
        if prev is None:
            id = self.InsertItemBefore(parent, 0, text, img, selImg)
        else:
            id = self.InsertItem(parent, prev, text, img, selImg)    
        self.SetPyData(id, data)            
        self.SetItemText(id, self.GetItemText(item, 1), 1)
        return id
        
    
    
class SysTrayMenu(eg.PluginClass):
    text = Text
    
    def __init__(self):
        self.menuItems = {}
        self.menuIds = {}
    
    
    def __start__(self, menuData=[]):
        if len(menuData) == 0:
            return
        menu =  eg.app.trayMenu
        self.menuItems[menu.PrependSeparator()] = None
        for name, kind, data in reversed(menuData):
            if kind == "item":
                id = wx.NewId()
                item = menu.Prepend(id, name)
                wx.EVT_MENU(menu, id, self.OnMenuItem)
                self.menuIds[id] = data
                self.menuItems[item] = None
            elif kind == "separator":
                item = menu.PrependSeparator()
                self.menuItems[item] = None
                
        
    def __stop__(self):
        for menuItem in self.menuItems:
            eg.app.trayMenu.RemoveItem(menuItem)
        self.menuItems.clear()
        self.menuIds.clear()
        
        
    @eg.LogIt
    def OnMenuItem(self, event):
        data = self.menuIds[event.GetId()]
        self.TriggerEvent(data)
        
    
    def Configure(self, menuData=[]):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        
        tree = TreeListCtrl(
            dialog, 
            -1,
            style = wx.TR_FULL_ROW_HIGHLIGHT 
                |wx.TR_DEFAULT_STYLE
                |wx.VSCROLL
        )
        tree.SetMinSize((10, 10))
        tree.AddColumn(text.labelHeader)
        tree.AddColumn(text.eventHeader)
        root = tree.AddRoot(self.name)
        for name, kind, data in menuData:
            item = tree.AppendItem(root, name)
            tree.SetItemText(item, str(data), 1)
            tree.SetPyData(item, kind)
        tree.SetColumnWidth(0, 200)
        tree.ExpandAll(root)
        
        @eg.LogIt
        def OnSelectionChanged(event):
            item = tree.GetSelection()
            if item == root:
                enableMoveFlag = False
                enableEditFlag = False
            elif tree.GetPyData(item) == "separator":
                enableMoveFlag = True
                enableEditFlag = False
            else:
                enableMoveFlag = True
                enableEditFlag = True
            upButton.Enable(enableMoveFlag)
            downButton.Enable(enableMoveFlag)
            deleteButton.Enable(enableMoveFlag)
            labelBox.Enable(enableEditFlag)
            eventBox.Enable(enableEditFlag)
            labelBox.SetLabel(tree.GetItemText(item, 0))
            eventBox.SetLabel(tree.GetItemText(item, 1))
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, OnSelectionChanged)
        
        # Delete button
        deleteButton = wx.Button(dialog, -1, text.deleteButton)
        deleteButton.Enable(False)
        def OnDelete(event):
            item = tree.GetSelection()
            next = tree.GetNextSibling(item)
            if not next.IsOk():
                next = tree.GetPrevSibling(item)
                if not next.IsOk():
                    next = tree.GetItemParent(item)
            tree.SelectItem(next)
            tree.Delete(item)
            tree.EnsureVisible(next)
        deleteButton.Bind(wx.EVT_BUTTON, OnDelete)
        
        # Up button
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        upButton = wx.BitmapButton(dialog, -1, bmp)
        upButton.Enable(False)
        def OnUp(event):
            item = tree.GetSelection()
            previous = tree.GetPrevSibling(item)
            if previous.IsOk():
                id = tree.GetPrevSibling(previous)
                if not id.IsOk():
                    id = None
                newId = tree.CopyItem(item, tree.GetItemParent(previous), id)
                tree.SelectItem(newId)
                tree.EnsureVisible(newId)
                tree.Delete(item)
        upButton.Bind(wx.EVT_BUTTON, OnUp)
        
        # Down button
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        downButton = wx.BitmapButton(dialog, -1, bmp)
        downButton.Enable(False)
        def OnDown(event):
            item = tree.GetSelection()
            next = tree.GetNext(item)
            if next is not None:
                newId = tree.CopyItem(item, tree.GetItemParent(next), next)
                tree.Delete(item)
                tree.SelectItem(newId)
                tree.EnsureVisible(newId)
        downButton.Bind(wx.EVT_BUTTON, OnDown)

        # Add menu item button
        addItemButton = wx.Button(dialog, -1, text.addItemButton)
        @eg.LogIt
        def OnAddItem(event):
            numStr = str(tree.GetCount() + 1)
            item = tree.AppendItem(root, text.unnamedLabel % numStr)
            tree.SetPyData(item, "item")
            tree.SetItemText(item, text.unnamedEvent % numStr, 1)
            tree.Expand(tree.GetItemParent(item))
            tree.SelectItem(item)
            tree.EnsureVisible(item)
            tree.Update()
        addItemButton.Bind(wx.EVT_BUTTON, OnAddItem)
        
        # Add separator button
        addSeparatorButton = wx.Button(dialog, -1, text.addSeparatorButton)
        def OnAddSeparator(event):
            item = tree.AppendItem(root, "---------")
            tree.SetPyData(item, "separator")
            tree.Expand(tree.GetItemParent(item))
            tree.SelectItem(item)
            tree.EnsureVisible(item)
            tree.Update()
        addSeparatorButton.Bind(wx.EVT_BUTTON, OnAddSeparator)
        
        # Label edit box
        labelBox = wx.TextCtrl(dialog, -1)
        def OnLabelTextChange(event):
            item = tree.GetSelection()
            tree.SetItemText(item, labelBox.GetValue(), 0)
        labelBox.Bind(wx.EVT_TEXT, OnLabelTextChange)
        
        # Event edit box
        eventBox = wx.TextCtrl(dialog, -1)
        def OnEventTextChange(event):
            item = tree.GetSelection()
            tree.SetItemText(item, eventBox.GetValue(), 1)
        eventBox.Bind(wx.EVT_TEXT, OnEventTextChange)
        
        # construction of the dialog with sizers
        staticBox = wx.StaticBox(dialog, -1, text.addBox)
        
        addSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        #addSizer = wx.BoxSizer(wx.VERTICAL)
        addSizer.Add(addItemButton, 0, wx.EXPAND)
        addSizer.Add((5, 5))
        addSizer.Add(addSeparatorButton, 0, wx.EXPAND)

        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(deleteButton, 0, wx.EXPAND)
        rightSizer.Add((5, 5), 1, wx.EXPAND)
        rightSizer.Add(upButton)
        rightSizer.Add(downButton, 0, wx.TOP, 5)
        rightSizer.Add((5, 5), 1, wx.EXPAND)
        rightSizer.Add(addSizer, 0, wx.EXPAND)
        
        editSizer = wx.FlexGridSizer(2, 2, 5, 5)
        editSizer.AddGrowableCol(1)
        staticText1 = wx.StaticText(dialog, -1, text.editLabel)
        editSizer.Add(staticText1, 0, wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(labelBox, 0, wx.EXPAND)
        staticText2 = wx.StaticText(dialog, -1, text.editEvent)
        editSizer.Add(staticText2, 0, wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(eventBox, 0, wx.EXPAND)
        
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(tree, 1, wx.EXPAND)
        leftSizer.Add(editSizer, 0, wx.EXPAND|wx.TOP, 5)
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer, 1, wx.EXPAND)
        mainSizer.Add((5, 5))
        mainSizer.Add(rightSizer, 0, wx.EXPAND)
        
        dialog.sizer.Add(mainSizer, 1, wx.EXPAND)
        
        next = tree.GetFirstChild(root)[0]
        if next.IsOk():
            tree.SelectItem(next)
        else:
            tree.SelectItem(root)
            
        if dialog.AffirmedShowModal():
            resultList = []
            def Traverse(item):
                child, cookie = tree.GetFirstChild(item)
                while child.IsOk():
                    name = tree.GetItemText(child, 0)
                    kind = tree.GetPyData(child)
                    data = tree.GetItemText(child, 1)
                    resultList.append((name, kind, data))
                    if tree.HasChildren(child):
                        Traverse(child)
                    child, cookie = tree.GetNextChild(item, cookie)
            Traverse(root)
            return (resultList, )
    
    
        