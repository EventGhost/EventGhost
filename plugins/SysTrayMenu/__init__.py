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
# $LastChangedDate: 2007-05-06 19:08:21 +0200 (So, 06 Mai 2007) $
# $LastChangedRevision: 127 $
# $LastChangedBy: bitmonster $

import eg

class PluginInfo(eg.PluginInfo):
    name = "System Tray Menu"
    description = (
        "Allows you to add custom menu entries to the tray menu of EventGhost."
    )
    author = "Bitmonster"
    version = "1.0.0"
    
import wx
import wx.gizmos


class Text:
    labelHeader = "Label"
    eventHeader = "Event"
    editLabel = "Label:"
    editEvent = "Event:"
    addButton = "Add"
    deleteButton = "Delete"
    unnamedLabel = "New Menu Item %s"
    unnamedEvent = "Event%s"
    
    
    
class TreeListCtrl(wx.gizmos.TreeListCtrl):
    
    def __init__(self, *args, **kwargs):
        wx.gizmos.TreeListCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    
    def OnSize(self, event):
        event.Skip()
        #self.Unbind(wx.EVT_SIZE)
        wx.CallAfter(self.OnSize2)
        
        
    def OnSize2(self):
        w, h = self.GetSizeTuple()
        self.SetColumnWidth(1, w - 204 - wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X))
        
        
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
            id = self.InsertItemBefore(parent, 0, text, img, selImg, data)
        else:
            id = self.InsertItem(parent, prev, text, img, selImg, data)                
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
        )
        tree.SetMinSize((10, 10))
        tree.AddColumn(text.labelHeader)
        tree.AddColumn(text.eventHeader)
        root = tree.AddRoot(self.name)
        for name, kind, data in menuData:
            if kind == "item":
                item = tree.AppendItem(root, name)
                tree.SetItemText(item, str(data), 1)
        tree.SetColumnWidth(0, 200)
        tree.ExpandAll(root)
        
        @eg.LogIt
        def OnSelectionChanged(event):
            item = tree.GetSelection()
            labelBox.Enable(item != root)
            eventBox.Enable(item != root)
            upButton.Enable(item != root)
            downButton.Enable(item != root)
            deleteButton.Enable(item != root)
            labelBox.SetLabel(tree.GetItemText(item, 0))
            eventBox.SetLabel(tree.GetItemText(item, 1))
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, OnSelectionChanged)
        
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

        # Add button
        addButton = wx.Button(dialog, -1, text.addButton)
        def OnAdd(event):
            numStr = str(tree.GetCount() + 1)
            item = tree.AppendItem(root, text.unnamedLabel % numStr)
            tree.SetItemText(item, text.unnamedEvent % numStr, 1)
            tree.Expand(tree.GetItemParent(item))
            tree.SelectItem(item)
            tree.EnsureVisible(item)
        addButton.Bind(wx.EVT_BUTTON, OnAdd)
        
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
        
        # Construction of the dialog with sizers
        buttonSizer1 = wx.BoxSizer(wx.VERTICAL)
        buttonSizer1.Add((5, 5), 1, wx.EXPAND)
        buttonSizer1.Add(upButton)
        buttonSizer1.Add(downButton)
        buttonSizer1.Add((5, 5), 1, wx.EXPAND)
        
        buttonSizer2 = wx.BoxSizer(wx.VERTICAL)
        buttonSizer2.Add(addButton)
        buttonSizer2.Add(deleteButton)
        
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.Add(buttonSizer1, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        buttonSizer.Add(buttonSizer2, 0)
        
        editSizer = wx.FlexGridSizer(2, 2, 5, 5)
        editSizer.AddGrowableCol(1)
        staticText1 = wx.StaticText(dialog, -1, text.editLabel)
        editSizer.Add(staticText1, 0, wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(labelBox, 0, wx.EXPAND)
        staticText2 = wx.StaticText(dialog, -1, text.editEvent)
        editSizer.Add(staticText2, 0, wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(eventBox, 0, wx.EXPAND)
        
        mainSizer = wx.FlexGridSizer(2, 2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(tree, 1, wx.EXPAND)
        mainSizer.Add(buttonSizer, 0, wx.LEFT|wx.EXPAND, 5)
        mainSizer.Add(editSizer, 0, wx.EXPAND|wx.TOP, 5)
        
        dialog.sizer.Add(mainSizer, 1, wx.EXPAND)
        
        next = tree.GetFirstChild(root)[0]
        if next.IsOk():
            tree.SelectItem(next)
        else:
            tree.SelectItem(root)
            
        if dialog.AffirmedShowModal():
            l = []
            def Traverse(item):
                child, cookie = tree.GetFirstChild(item)
                while child.IsOk():
                    data = tree.GetItemText(child, 0), "item", tree.GetItemText(child, 1)
                    l.append(data)
                    if tree.HasChildren(child):
                        Traverse(child)
                    child, cookie = tree.GetNextChild(item, cookie)
            Traverse(root)
            return (l,)
    
    
        