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
import wx.gizmos

# Local imports
import eg

class NamespaceTree(wx.gizmos.TreeListCtrl):
    def __init__(self, parent, namespace):
        self.namespace = namespace
        wx.gizmos.TreeListCtrl.__init__(
            self,
            parent,
            style=(
                wx.TR_FULL_ROW_HIGHLIGHT |
                wx.TR_DEFAULT_STYLE |
                wx.VSCROLL |
                wx.ALWAYS_SHOW_SB  #|
                #wx.CLIP_CHILDREN
            )
        )
        self.AddColumn("Name")
        self.AddColumn("Type")
        self.AddColumn("Value")

    def FillTree(self):
        root = self.AddRoot("Root")
        for name, value in self.namespace.__dict__.items():
            item = self.AppendItem(root, name)
            typeStr = str(type(value))
            if typeStr.startswith("<class "):
                typeStr = "class"
            else:
                typeStr = typeStr[7:-2]
            self.SetItemText(item, typeStr, 1)
            valueStr = repr(value)
            self.SetItemText(item, valueStr, 2)
            self.SetPyData(item, value)
        self.Expand(root)

    @classmethod
    def Test(cls):
        dialog = eg.Dialog(
            None,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        tree = cls(dialog, eg)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tree, 1, wx.EXPAND)
        tree.FillTree()
        dialog.SetSizerAndFit(sizer)
        dialog.ShowModal()
        dialog.Destroy()
