# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx


class Text:
    mesg = "Please select the folder you want to export"

text = Text


class ExportDialog(eg.TaskletDialog):

    def Configure(self):
        self.foundId = None
        style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        eg.TaskletDialog.__init__(self, None, -1, title="Export", style=style)
        staticText = wx.StaticText(self, -1, text.mesg)

        filterClasses = (eg.FolderItem, )#eg.MacroItem)
        def filterFunc(obj):
            return isinstance(obj, filterClasses)

        tree = eg.TreeItemBrowseCtrl(self, filterFunc) #, multiSelect=True)
        #tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.UnselectAll()

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL), True)

        mainSizer = eg.VBoxSizer(
            (staticText, 0, wx.EXPAND|wx.ALL, 5),
            (tree, 1, wx.EXPAND),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(mainSizer)
        self.SetAutoLayout(True)
        #mainSizer.Fit(self)
        #self.SetMinSize(self.GetSize())
        self.SetSize((450, 400))
        while self.Affirmed():
            items = tree.GetSelections()
            GetPyData = tree.GetPyData
            self.SetResult([GetPyData(item) for item in items])

