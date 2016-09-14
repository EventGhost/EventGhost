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

class MacroSelectButton(wx.Window):
    def __init__(self, parent, label, title, mesg, treeLink=None):
        if treeLink is None:
            treeLink = eg.TreeLink(eg.Utils.GetTopLevelWindow(parent).treeItem)
        self.treeLink = treeLink
        self.macro = treeLink.target
        if self.macro is None:
            macroName = ""
        else:
            macroName = self.macro.name
        self.title = title
        self.mesg = mesg
        wx.Window.__init__(self, parent, -1)
        self.textBox = eg.StaticTextBox(self, -1, macroName, size=(200, -1))
        self.button = wx.Button(self, -1, label)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.textBox, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.button, 0, wx.LEFT, 5)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Layout()

    def GetValue(self):
        self.treeLink.SetTarget(self.macro)
        return self.treeLink

    @eg.AsTasklet
    def OnButton(self, dummyEvent):
        result = eg.TreeItemBrowseDialog.GetModalResult(
            self.title,
            self.mesg,
            self.macro,
            (eg.MacroItem,),
            parent=self
        )
        if result:
            macro = result[0]
            self.textBox.SetLabel(macro.name)
            self.macro = macro
            self.ProcessEvent(
                wx.CommandEvent(wx.EVT_TEXT.evtType[0], self.GetId())
            )

    def OnSetFocus(self, dummyEvent):
        self.button.SetFocus()

    def OnSize(self, dummyEvent):
        if self.GetAutoLayout():
            self.Layout()
