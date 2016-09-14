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

class StaticTextBox(wx.PyWindow):
    def __init__(self, parent, id=-1, label='', pos=(-1, -1), size=(-1, -1)):
        wx.PyWindow.__init__(
            self,
            parent,
            id,
            pos,
            size,
            style=wx.SUNKEN_BORDER
        )
        self.SetMinSize(self.GetSize())
        sizer = wx.BoxSizer(wx.VERTICAL)
        textCtrl = wx.TextCtrl(
            self,
            -1,
            label,
            style=(
                wx.TE_MULTILINE |
                wx.TE_NO_VSCROLL |
                wx.NO_BORDER |
                wx.TE_READONLY
            )
        )
        textCtrl.SetBackgroundColour(self.GetBackgroundColour())
        #sizer.Add((0,0), 1, wx.EXPAND)
        sizer.Add(textCtrl, 0, wx.EXPAND | wx.ALL, 3)
        sizer.Add((0, 0), 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.textCtrl = textCtrl

    def AcceptsFocus(self):
        return False

    def GetValue(self):
        return self.textCtrl.GetLabel()

    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

    def SetLabel(self, label):
        self.textCtrl.SetLabel(label)

    def SetValue(self, label):
        self.textCtrl.SetLabel(label)
