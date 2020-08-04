# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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
import eg


def h_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)

    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


class IrCodeCtrl(wx.Panel):

    def __init__(
        self,
        parent,
        id,
        decoder,
        size=wx.DefaultSize,
        pos=wx.DefaultPosition,
        style=wx.BORDER_NONE
    ):

        wx.Panel.__init__(self, parent, id, size=size, pos=pos, style=style)
        self.codes = sorted([code for d in decoder for code in d], key=lambda x: x.name)
        choices = list(code.name for code in decoder)

        self.ctrl = wx.Choice(self, -1, choices=choices)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ctrl, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def SetStringSelection(self, value):
        if value in self.ctrl.GetItems():
            self.ctrl.SetStringSelection(value)
        else:
            self.ctrl.SetSelection(0)

    def SetSelection(self, value):
        if value < len(self.ctrl.GetItems()):
            self.ctrl.SetSelection(value)
        else:
            self.ctrl.SetSelection(0)

    def GetStringSelection(self):
        return self.ctrl.GetStringSelection()

    def GetSelection(self):
        return self.ctrl.GetSelection()

    def GetValue(self):
        return self.codes[self.ctrl.GetSelection()]

