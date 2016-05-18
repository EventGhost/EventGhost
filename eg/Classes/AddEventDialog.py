# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

gLastSelected = None

class Config(eg.PersistentData):
    position = None
    size = (550, 400)
    splitPosition = 210


class Text(eg.TranslatableStrings):
    title = "Select an event to add..."
    descriptionLabel = "Description"


class AddEventDialog(eg.TaskletDialog):
    @eg.LogItWithReturn
    def Configure(self, parent):
        global gLastSelected
        self.resultData = None
        eg.TaskletDialog.__init__(
            self,
            parent,
            -1,
            Text.title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        )
        splitterWindow = wx.SplitterWindow(
            self,
            -1,
            style=(
                wx.SP_LIVE_UPDATE |
                wx.CLIP_CHILDREN |
                wx.NO_FULL_REPAINT_ON_RESIZE
            )
        )

        style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT
        tree = wx.TreeCtrl(splitterWindow, -1, style=style)
        tree.SetMinSize((100, 100))
        tree.SetImageList(eg.Icons.gImageList)
        self.tree = tree

        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)
        tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnStartDrag)

        rightPanel = self.rightPanel = wx.Panel(splitterWindow)
        rightSizer = self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)
        rightPanel.SetAutoLayout(True)

        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        rightSizer.Add(nameText, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label=Text.descriptionLabel),
            wx.VERTICAL
        )
        self.docText = eg.HtmlWindow(rightPanel)
        self.docText.SetBorders(2)

        staticBoxSizer.Add(self.docText, 1, wx.EXPAND)
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND, 5)

        splitterWindow.SplitVertically(self.tree, rightPanel)
        splitterWindow.SetMinimumPaneSize(60)
        splitterWindow.UpdateSize()

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL), True)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitterWindow, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(mainSizer)
        minSize = mainSizer.GetMinSize()
        self.SetMinSize(minSize)
        self.SetSize(Config.size)
        splitterWindow.SetSashPosition(Config.splitPosition)
        if Config.position is not None:
            self.SetPosition(Config.position)
        self.ReloadTree()
        while self.Affirmed():
            self.SetResult(self.resultData)
        item = tree.GetSelection()
        gLastSelected = tree.GetPyData(item)
        Config.size = self.GetSizeTuple()
        Config.position = self.GetPositionTuple()
        Config.splitPosition = splitterWindow.GetSashPosition()

    def FillTree(self):
        tree = self.tree
        for plugin in eg.pluginList:
            eventList = plugin.info.eventList
            if eventList is None:
                continue
            item = tree.AppendItem(self.root, plugin.name)
            tree.SetPyData(item, plugin.info)
            tree.SetItemImage(item, plugin.info.icon.folderIndex)

            for eventName, description in eventList:
                data = EventInfo(eventName, description, plugin.info)
                tmp = tree.AppendItem(item, eventName)
                tree.SetPyData(tmp, data)
                tree.SetItemImage(tmp, data.icon.index)

    def OnActivated(self, event):
        item = self.tree.GetSelection()
        data = self.tree.GetPyData(item)
        if isinstance(data, EventInfo):
            self.OnOK()
        else:
            event.Skip()

    def OnCollapsed(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = False

    def OnExpanded(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = True

    @eg.LogItWithReturn
    def OnStartDrag(self, event):
        item = self.tree.GetPyData(event.GetItem())
        text = item.info.eventPrefix + "." + item.name
        # create our own data format and use it in a
        # custom data object
        customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        customData.SetData(text.encode("utf-8"))

        # And finally, create the drop source and begin the drag
        # and drop opperation
        dropSource = wx.DropSource(self)
        dropSource.SetData(customData)
        result = dropSource.DoDragDrop(wx.Drag_DefaultMove)
        if result == wx.DragMove:
            self.Refresh()

    def OnSelectionChanged(self, event):
        item = event.GetItem()
        if not item.IsOk():
            return
        data = self.tree.GetPyData(item)
        if isinstance(data, EventInfo):
            self.resultData = data.info.eventPrefix + "." + data.name
            self.buttonRow.okButton.Enable(True)
            path = data.info.path
        else:
            self.resultData = None
            self.buttonRow.okButton.Enable(False)
            path = data.path
        self.nameText.SetLabel(data.name)
        self.docText.SetBasePath(path)
        self.docText.SetPage(data.description)

    def ReloadTree(self):
        tree = self.tree
        tree.DeleteAllItems()
        self.root = tree.AddRoot("Functions")
        self.lastSelectedTreeItem = None
        self.FillTree()

        if self.lastSelectedTreeItem:
            item = self.lastSelectedTreeItem
            while True:
                item = tree.GetItemParent(item)
                if item == self.root:
                    break
                tree.EnsureVisible(item)
            tree.SelectItem(self.lastSelectedTreeItem)


class EventInfo:
    icon = eg.Icons.EVENT_ICON

    def __init__(self, name, description, info):
        self.name = name
        if description:
            self.description = description
        else:
            self.description = ""
        self.info = info
