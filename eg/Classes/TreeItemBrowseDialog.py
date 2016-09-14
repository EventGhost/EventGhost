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

class TreeItemBrowseDialog(eg.TaskletDialog):
    def Configure(
        self,
        title,
        text,
        searchItem,
        resultClasses,
        filterClasses=(eg.FolderItem, eg.MacroItem),
        parent=None,
    ):
        self.resultData = searchItem
        self.resultClasses = resultClasses
        self.foundId = None
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        eg.TaskletDialog.__init__(self, parent, -1, title=title, style=style)
        staticText = wx.StaticText(self, -1, text)
        staticText.Wrap(430)

        def filterFunc(obj):
            return isinstance(obj, filterClasses)

        tree = eg.TreeItemBrowseCtrl(self, filterFunc, selectItem=searchItem)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        self.treeCtrl = tree

        self.buttonRow = eg.ButtonRow(self, (wx.ID_CANCEL, wx.ID_OK), True)
        mainSizer = eg.VBoxSizer(
            (staticText, 0, wx.EXPAND | wx.ALL, 5),
            (tree, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5),
            (self.buttonRow.sizer, 0, wx.EXPAND),
        )

        self.SetSizerAndFit(mainSizer)
        self.SetSize((450, 400))

        if not searchItem:
            self.buttonRow.okButton.Enable(False)
        while self.Affirmed():
            self.SetResult(self.resultData)

    def GetValue(self):
        return self.resultData

    def OnSelectionChanged(self, event):
        item = event.GetItem()
        if item.IsOk():
            obj = self.treeCtrl.GetPyData(item)
            if isinstance(obj, self.resultClasses):
                self.resultData = obj
                self.buttonRow.okButton.Enable(True)
            else:
                self.buttonRow.okButton.Enable(False)
        event.Skip()
