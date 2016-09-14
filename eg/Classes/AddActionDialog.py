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

class Config(eg.PersistentData):
    position = None
    size = (550, 400)
    splitPosition = 210


class Text(eg.TranslatableStrings):
    title = "Add Action..."
    descriptionLabel = "Description"


class AddActionDialog(eg.TaskletDialog):
    lastSelectedDataItem = None

    @eg.LogItWithReturn
    def Configure(self, parent):
        self.resultData = None
        self.lastSelectedTreeItem = None
        eg.TaskletDialog.__init__(
            self,
            parent,
            -1,
            Text.title,
            style=(
                wx.DEFAULT_DIALOG_STYLE |
                wx.RESIZE_BORDER |
                wx.THICK_FRAME
            )
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
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)
        self.tree = tree

        rightPanel = wx.Panel(splitterWindow)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
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

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL), True)

        staticBoxSizer.Add(self.docText, 1, wx.EXPAND)
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND, 5)

        splitterWindow.SplitVertically(self.tree, rightPanel)
        splitterWindow.SetMinimumPaneSize(60)
        splitterWindow.UpdateSize()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitterWindow, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(mainSizer)
        minSize = mainSizer.GetMinSize()
        self.SetMinSize(minSize)
        self.SetSize(Config.size)
        splitterWindow.SetSashPosition(Config.splitPosition)
        self.FillTree()
        if Config.position is not None:
            self.SetPosition(Config.position)
        while self.Affirmed():
            self.SetResult(self.resultData)

        item = self.tree.GetSelection()
        self.__class__.lastSelectedDataItem = self.tree.GetPyData(item)
        Config.size = self.GetSizeTuple()
        Config.position = self.GetPositionTuple()
        Config.splitPosition = splitterWindow.GetSashPosition()

    def FillTree(self):
        """
        Fills the action-picker tree with data.
        """
        tree = self.tree
        tree.SetImageList(eg.Icons.gImageList)

        root = tree.AddRoot("Root")
        self.lastSelectedTreeItem = None
        self.RecurseActionGroup(eg.actionGroup, tree, root)

        if self.lastSelectedTreeItem:
            treeItem = self.lastSelectedTreeItem
            while True:
                treeItem = tree.GetItemParent(treeItem)
                if treeItem == root:
                    break
                tree.EnsureVisible(treeItem)
            tree.SelectItem(self.lastSelectedTreeItem)

    def OnActivated(self, event):
        """
        Process wx.EVT_TREE_ITEM_ACTIVATED events.
        """
        treeItem = self.tree.GetSelection()
        itemData = self.tree.GetPyData(treeItem)
        if isinstance(itemData, eg.ActionGroup):
            event.Skip()
        else:
            self.OnOK(wx.CommandEvent())

    def OnCollapsed(self, event):
        """
        Process wx.EVT_TREE_ITEM_COLLAPSED events.
        """
        self.tree.GetPyData(event.GetItem()).expanded = False

    def OnExpanded(self, event):
        """
        Process wx.EVT_TREE_ITEM_EXPANDED events.
        """
        self.tree.GetPyData(event.GetItem()).expanded = True

    def OnSelectionChanged(self, event):
        """
        Process wx.EVT_TREE_SEL_CHANGED events.
        """
        treeItem = event.GetItem()
        if not treeItem.IsOk():
            return
        itemData = self.tree.GetPyData(treeItem)
        if isinstance(itemData, eg.ActionGroup):
            self.resultData = None
            self.buttonRow.okButton.Enable(False)
        else:
            self.resultData = itemData
            self.buttonRow.okButton.Enable(True)
        self.nameText.SetLabel(itemData.name)
        self.docText.SetBasePath(itemData.plugin.info.path)
        self.docText.SetPage(itemData.description)

    def RecurseActionGroup(self, actionGroup, tree, parentTreeItem):
        """
        Recurses an eg.ActionGroup and adds the items to the TreeCtrl.
        """
        for dataItem in actionGroup.items:
            if isinstance(dataItem, eg.ActionGroup):
                # the dataItem is an eg.ActionGroup instance
                isActionGroup = True
                if not len(dataItem.items):
                    # don't add empty ActionGroups
                    continue
                iconIndex = dataItem.icon.folderIndex
            else:
                # the dataItem is an action
                isActionGroup = False
                iconIndex = dataItem.info.icon.index
            newTreeItem = tree.AppendItem(parentTreeItem, dataItem.name)
            tree.SetPyData(newTreeItem, dataItem)
            tree.SetItemImage(newTreeItem, iconIndex)
            if isActionGroup:
                self.RecurseActionGroup(dataItem, tree, newTreeItem)
                if dataItem.expanded:
                    tree.Expand(newTreeItem)
            if dataItem == self.lastSelectedDataItem:
                self.lastSelectedTreeItem = newTreeItem
