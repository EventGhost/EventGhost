# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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

import eg

eg.RegisterPlugin(
    name = "System Tray Menu",
    description = (
        "Allows you to add custom menu entries to the tray menu of EventGhost."
    ),
    author = "Bitmonster",
    version = "1.0",
    guid = "{842BFFE8-DCB9-4C72-9877-AB2EF49794C5}",
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


import wx
import wx.gizmos
import types


class MenuItemData:
    pass

class MenuTreeListCtrl(wx.gizmos.TreeListCtrl):

    def __init__(self, parent, text, menuData, selectedItem=None):
        self.highestMenuId = 0
        wx.gizmos.TreeListCtrl.__init__(
            self,
            parent,
            style = wx.TR_FULL_ROW_HIGHLIGHT
                |wx.TR_DEFAULT_STYLE
                |wx.VSCROLL
                |wx.ALWAYS_SHOW_SB
                |wx.CLIP_CHILDREN
        )
        self.SetMinSize((10, 150))
        self.AddColumn(text.labelHeader)
        self.AddColumn(text.eventHeader)
        root = self.AddRoot(text.name)
        for data in menuData:
            name, kind, eventName, menuId = data
            if menuId > self.highestMenuId:
                self.highestMenuId = menuId
            eventName = data[2]
            item = self.AppendItem(root, name)
            self.SetItemText(item, eventName, 1)
            self.SetPyData(item, data)
            if menuId == selectedItem:
                self.SelectItem(item)

        self.SetColumnWidth(0, 200)
        self.ExpandAll(root)

        self.__inSizing = False
        self.GetMainWindow().Bind(wx.EVT_SIZE, self.OnSize)


    def GetNewMenuId(self):
        newMenuId = self.highestMenuId + 1
        self.highestMenuId = newMenuId
        return newMenuId


    def OnSize(self, event):
        event.Skip()
        if not self.__inSizing:
            self.__inSizing = True
            wx.CallAfter(self.OnSize2)


    def OnSize2(self):
        w, h = self.GetMainWindow().GetClientSize()
        newWidth = w - self.GetColumnWidth(0)
        if self.GetColumnWidth(1) != newWidth:
            self.SetColumnWidth(1, newWidth)
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


    def GetSelectedId(self):
        selectedId = self.GetSelection()
        data = self.GetPyData(selectedId)
        if data is not None:
            return data[3]



class SysTrayMenu(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddAction(Enable)
        self.AddAction(Disable)


    def Compile(self, menuData=[]):
        self.menuIdToData = {}
        # convert menuData to the new format
        newData = []
        i = 0
        for data in menuData:
            if len(data) < 4:
                name, kind, eventName  = data
                i += 1
                data = (name, kind, eventName, i)
            newData.append(data)
            self.menuIdToData[data[3]] = data
        self.menuData = newData
        return newData


    def __start__(self, dummy=None):
        self.wxIdToData = {}
        self.menuIdToWxItem = {}
        self.menuIdToData = {}
        if len(self.menuData) == 0:
            return
        menu =  eg.taskBarIcon.menu
        self.menuIdToWxItem[-1] = menu.PrependSeparator()
        for data in reversed(self.menuData):
            name, kind, eventName, menuId = data
            if kind == "item":
                wxId = wx.NewId()
                wxItem = menu.Prepend(wxId, name)
                wx.EVT_MENU(menu, wxId, self.OnMenuItem)
                self.wxIdToData[wxId] = data
            elif kind == "separator":
                wxItem = menu.PrependSeparator()
            self.menuIdToWxItem[menuId] = wxItem
            self.menuIdToData[menuId] = data


    def __stop__(self):
        for item in self.menuIdToWxItem.values():
            eg.taskBarIcon.menu.RemoveItem(item)
        self.menuIdToWxItem.clear()
        self.wxIdToData.clear()


    @eg.LogIt
    def OnMenuItem(self, event):
        data = self.wxIdToData[event.GetId()]
        self.TriggerEvent(data[2])


    def Configure(self, menuData=[]):
        menuData = self.Compile(menuData)
        panel = eg.ConfigPanel(resizable=True)
        text = self.text

        tree = MenuTreeListCtrl(panel, text, menuData)
        root = tree.GetRootItem()

        @eg.LogIt
        def OnSelectionChanged(dummyEvent):
            itemType = 0
            item = tree.GetSelection()
            if item == root:
                enableMoveFlag = False
                enableEditFlag = False
            elif tree.GetPyData(item)[1] == "separator":
                enableMoveFlag = True
                enableEditFlag = False
                itemType = 2
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
            #itemTypeCtrl.SetSelection(itemType)
            #event.Skip()
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, OnSelectionChanged)

        # Delete button
        deleteButton = wx.Button(panel, -1, text.deleteButton)
        deleteButton.Enable(False)
        def OnDelete(dummyEvent):
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
        upButton = wx.BitmapButton(panel, -1, bmp)
        upButton.Enable(False)
        def OnUp(dummyEvent):
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
        downButton = wx.BitmapButton(panel, -1, bmp)
        downButton.Enable(False)
        def OnDown(dummyEvent):
            item = tree.GetSelection()
            nextId = tree.GetNext(item)
            if nextId is not None:
                newId = tree.CopyItem(item, tree.GetItemParent(nextId), nextId)
                tree.Delete(item)
                tree.SelectItem(newId)
                tree.EnsureVisible(newId)
        downButton.Bind(wx.EVT_BUTTON, OnDown)

        # Add menu item button
        addItemButton = wx.Button(panel, -1, text.addItemButton)
        @eg.LogIt
        def OnAddItem(dummyEvent):
            numStr = str(tree.GetCount() + 1)
            item = tree.AppendItem(root, text.unnamedLabel % numStr)
            data = ("", "item", "", tree.GetNewMenuId())
            tree.SetPyData(item, data)
            tree.SetItemText(item, text.unnamedEvent % numStr, 1)
            tree.Expand(tree.GetItemParent(item))
            tree.SelectItem(item)
            tree.EnsureVisible(item)
            tree.Update()
        addItemButton.Bind(wx.EVT_BUTTON, OnAddItem)

        # Add separator button
        addSeparatorButton = wx.Button(panel, -1, text.addSeparatorButton)
        def OnAddSeparator(dummyEvent):
            item = tree.AppendItem(root, "---------")
            tree.SetPyData(item, ("", "separator", "", tree.GetNewMenuId()))
            tree.Expand(tree.GetItemParent(item))
            tree.SelectItem(item)
            tree.EnsureVisible(item)
            tree.Update()
        addSeparatorButton.Bind(wx.EVT_BUTTON, OnAddSeparator)

        # Label edit box
        labelBox = wx.TextCtrl(panel, -1)
        def OnLabelTextChange(event):
            item = tree.GetSelection()
            tree.SetItemText(item, labelBox.GetValue(), 0)
            event.Skip()
        labelBox.Bind(wx.EVT_TEXT, OnLabelTextChange)

        # Event edit box
        eventBox = wx.TextCtrl(panel, -1)
        def OnEventTextChange(event):
            item = tree.GetSelection()
            tree.SetItemText(item, eventBox.GetValue(), 1)
            event.Skip()
        eventBox.Bind(wx.EVT_TEXT, OnEventTextChange)

        # Item type control
        #choices = ["Menu item", "Check menu item", "Separator"]
        #itemTypeCtrl = wx.Choice(dialog, choices=choices)

        # construction of the dialog with sizers
        staticBox = wx.StaticBox(panel, -1, text.addBox)
        addSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        addSizer.Add(addItemButton, 0, wx.EXPAND)
        addSizer.Add((5, 5))
        addSizer.Add(addSeparatorButton, 0, wx.EXPAND)

        editSizer = wx.FlexGridSizer(2, 2, 5, 5)
        editSizer.AddGrowableCol(1)
        editSizer.AddMany((
            (panel.StaticText(text.editLabel), 0, wx.ALIGN_CENTER_VERTICAL),
            (labelBox, 0, wx.EXPAND),
            (panel.StaticText(text.editEvent), 0, wx.ALIGN_CENTER_VERTICAL),
            (eventBox, 0, wx.EXPAND),
        ))

        mainSizer = eg.HBoxSizer(
            (
                eg.VBoxSizer(
                    (tree, 1, wx.EXPAND),
                    (editSizer, 0, wx.EXPAND|wx.TOP, 5),
                ), 1, wx.EXPAND
            ),
            ((5, 5)),
            (
                eg.VBoxSizer(
                    (deleteButton, 0, wx.EXPAND),
                    ((5, 5), 1, wx.EXPAND),
                    (upButton),
                    (downButton, 0, wx.TOP, 5),
                    ((5, 5), 1, wx.EXPAND),
                    (addSizer, 0, wx.EXPAND),
                ), 0, wx.EXPAND
            ),
        )
        panel.sizer.Add(mainSizer, 1, wx.EXPAND)

        nextId = tree.GetFirstChild(root)[0]
        if nextId.IsOk():
            tree.SelectItem(nextId)
        else:
            tree.SelectItem(root)

        while panel.Affirmed():
            resultList = []
            def Traverse(item):
                child, cookie = tree.GetFirstChild(item)
                while child.IsOk():
                    name, kind, eventString, menuId = tree.GetPyData(child)
                    name = tree.GetItemText(child, 0)
                    eventString = tree.GetItemText(child, 1)
                    resultList.append((name, kind, eventString, menuId))
                    if tree.HasChildren(child):
                        Traverse(child)
                    child, cookie = tree.GetNextChild(item, cookie)
            Traverse(root)
            self.Compile(resultList)
            panel.SetResult(resultList)



class Enable(eg.ActionBase):

    class text:
        name = "Enable Item"
        description = "Enables a menu item."

    def __call__(self, menuId):
        item = self.plugin.menuIdToWxItem.get(menuId, None)
        if item is not None:
            item.Enable(True)


    def GetLabel(self, menuId):
        return self.name + ": " + self.plugin.menuIdToData[menuId][0]


    def Configure(self, menuId=None):
        plugin = self.plugin
        panel = eg.ConfigPanel()
        tree = MenuTreeListCtrl(panel, plugin.text, plugin.menuData, menuId)
        panel.sizer.Add(tree, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(tree.GetSelectedId())



class Disable(Enable):

    class text:
        name = "Disable Item"
        description = "Disables a menu item."

    def __call__(self, menuId):
        item = self.plugin.menuIdToWxItem.get(menuId, None)
        if item is not None:
            item.Enable(False)

