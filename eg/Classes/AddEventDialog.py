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

gLastSelected = None

class Config(eg.PersistentData):
    position = None
    size = (550, 400)
    splitPosition = 210


class Text(eg.TranslatableStrings):
    title = "Add Event..."
    descriptionLabel = "Description"
    noDescription = "<i>No description available</i>"
    userEventLabel = "Manually enter event"
    userEvent = "If an event is not in the list of available events," \
                " it can be manually entered here."


class AddEventDialog(eg.TaskletDialog):
    @eg.LogItWithReturn
    def Configure(self, parent):
        global gLastSelected
        self.resultData = None
        super(AddEventDialog, self).__init__(
            parent=parent, id=wx.ID_ANY, title=Text.title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
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

        leftPanel = wx.Panel(splitterWindow)
        self.tree = tree = wx.TreeCtrl(leftPanel, -1,
                           style=wx.TR_DEFAULT_STYLE |
                                 wx.TR_HIDE_ROOT |
                                 wx.TR_FULL_ROW_HIGHLIGHT
                           )
        tree.SetMinSize((100, 100))
        tree.SetImageList(eg.Icons.gImageList)

        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)
        tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnStartDrag)
        tree.Bind(wx.EVT_SET_FOCUS, self.OnFocusTree)

        self.userEvent = wx.TextCtrl(leftPanel, wx.ID_ANY,
                                     style=wx.TE_PROCESS_ENTER)
        self.userEvent.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
        self.userEvent.Bind(wx.EVT_SET_FOCUS, self.OnFocusUserEvent)

        leftSizer =  wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(tree, 1, wx.EXPAND)
        leftSizer.Add(self.userEvent, 0, wx.EXPAND)
        leftPanel.SetSizer(leftSizer)

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

        splitterWindow.SplitVertically(leftPanel, rightPanel)
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
            if not eventList:
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
            self.OnOK(event)
        else:
            event.Skip()

    def OnCollapsed(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = False

    def OnExpanded(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = True

    def OnFocusTree(self, event):
        item = self.tree.GetSelection()
        try:
            self.DoSelectionChanged(item)
        except AssertionError:
            pass
        event.Skip()

    def OnFocusUserEvent(self, event):
        self.nameText.SetLabel(Text.userEventLabel)
        self.docText.SetBasePath("")
        self.docText.SetPage(Text.userEvent)
        self.resultData = None
        self.buttonRow.okButton.Enable(False)
        event.Skip()

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
        self.DoSelectionChanged(item)

    def DoSelectionChanged(self, item):
        try:
            data = self.tree.GetPyData(item)
        except RuntimeError:
            return
        if isinstance(data, EventInfo):
            self.resultData = data.info.eventPrefix + "." + data.name
            self.buttonRow.okButton.Enable(True)
            self.userEvent.SetValue(self.resultData)
            path = data.info.path
        else:
            self.resultData = None
            self.buttonRow.okButton.Enable(False)
            self.userEvent.SetValue("")
            path = data.path
        self.nameText.SetLabel(data.name)
        self.docText.SetBasePath(path)
        self.docText.SetPage(
            data.description if data.description else Text.noDescription
        )

    def OnTextEnter(self, event):
        value = event.GetString()
        if value:
            self.resultData = value
            self.buttonRow.okButton.Enable(True)
            wx.CallAfter(self.buttonRow.okButton.SetFocus)
        else:
            self.resultData = None
            self.buttonRow.okButton.Enable(False)

    def ReloadTree(self):
        global gLastSelected
        tree = self.tree
        tree.DeleteAllItems()
        self.root = tree.AddRoot("Functions")
        self.FillTree()
        if gLastSelected:
            item = self.FindItemByText(gLastSelected.name)
            if item.IsOk():
                tree.EnsureVisible(item)
                tree.SelectItem(item)

    def FindItemByText(self, text):
        tree = self.tree

        def FindItem(item, text):
            subItem, cookie = tree.GetFirstChild(item)
            while subItem.IsOk():
                if tree.GetItemData(subItem).Data.name == text:
                    return subItem
                FindItem(subItem, text)
                subItem = tree.GetNextSibling(subItem)
            return wx.TreeItemId()

        item, cookie = tree.GetFirstChild(tree.GetRootItem())
        return FindItem(item, text)


class EventInfo:
    icon = eg.Icons.EVENT_ICON

    def __init__(self, name, description, info):
        self.name = name
        if description:
            self.description = description
        else:
            self.description = ""
        self.info = info
