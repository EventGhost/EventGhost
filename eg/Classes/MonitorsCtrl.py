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
from win32api import EnumDisplayMonitors as Edm

# Local imports
import eg

class MonitorsCtrl(wx.Panel):
    def __init__(
        self,
        parent = None,
        id = -1,
        label = "",
        pos = (-1, -1),
        size = (-1, -1),
        style = wx.BORDER_SIMPLE,
        name = "Monitors",
        background = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)

    ):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
        b1 = 2
        b2 = 3
        b3 = self.GetWindowBorderSize()[1]
        lbl = wx.StaticText(self, -1, eg.text.General.monitorsLabel, pos = ((b2, b1)))
        lbl.Enable(False)
        monsCtrl = MonsListCtrl(self, ((b2, 2 * b1 + lbl.GetSize()[1])))
        self.SetBackgroundColour(wx.Colour(*background))
        monsCtrl.SetBackgroundColour(wx.Colour(*background))
        w, h = monsCtrl.GetRealSize()
        self.size = (w + 2 * b2 + 2, h + lbl.GetSize()[1] + 2 * b1 + b2 + b3)
        self.SetMinSize(self.size)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, dummyEvent):
        self.SetSize(self.size)


class MonsListCtrl(wx.ListCtrl):
    def __init__(self, parent, pos, size = wx.DefaultSize):
        ID = wx.NewId()
        style = wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.LC_SINGLE_SEL
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        mons = [(i[0], i[1], i[2] - i[0], i[3] - i[1]) for i in [j[2] for j in Edm()]]
        for j, header in enumerate(eg.text.General.monitorsHeader):
            self.InsertColumn(j, header, wx.LIST_FORMAT_RIGHT)
            self.SetColumnWidth(j, wx.LIST_AUTOSIZE_USEHEADER)
        for i, mon in enumerate(mons):
            self.InsertStringItem(i, str(i + 1))
            self.SetStringItem(i, 1, str(mon[0]))
            self.SetStringItem(i, 2, str(mon[1]))
            self.SetStringItem(i, 3, str(mon[2]))
            self.SetStringItem(i, 4, str(mon[3]))
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        self.hh = rect[1]  #header height
        self.ih = rect[3]  #item height
        size = self.GetRealSize()
        self.SetMinSize(size)
        self.SetSize(size)

    def GetRealSize(self):
        w = 0
        for i in range(self.GetColumnCount()):
            w += self.GetColumnWidth(i)
        border = self.GetWindowBorderSize()
        w += border[0]
        return (w, self.hh + border[1] + self.GetItemCount() * self.ih)
