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

class Slider(wx.Window):
    def __init__(
        self,
        parent,
        id = -1,
        value = None,
        min = None,
        max = None,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = 0,
        valueLabel = None,
        minLabel = None,
        maxLabel = None,
        levelCallback = None
    ):
        if minLabel is None:
            minLabel = str(min)
        if maxLabel is None:
            maxLabel = str(max)
        if valueLabel is None:
            valueLabel = "%(1)i"
        self.valueLabel = valueLabel
        self.levelCallback = levelCallback
        wx.Window.__init__(self, parent, id, pos, size, style)
        self.slider = wx.Slider(
            self,
            -1,
            value,
            min,
            max,
            style = style
        )
        st1 = wx.StaticText(self, -1, minLabel)
        self.valueLabelCtrl = wx.StaticText(self, -1, valueLabel)
        st2 = wx.StaticText(self, -1, maxLabel)

        sizer = wx.GridBagSizer()
        sizer.AddMany([
            (self.slider, (0, 0), (1, 3), wx.EXPAND),
            (st1, (1, 0), (1, 1), wx.ALIGN_LEFT),
            (self.valueLabelCtrl, (1, 1), (1, 1), wx.ALIGN_CENTER_HORIZONTAL),
            (st2, (1, 2), (1, 1), wx.ALIGN_RIGHT),
        ])
        sizer.AddGrowableCol(1, 1)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SCROLL, self.OnScrollChanged)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.OnScrollChanged()

    def GetValue(self):
        return self.slider.GetValue()

    def OnScrollChanged(self, dummyEvent=None):
        value = self.slider.GetValue()
        if self.levelCallback is None:
            self.valueLabelCtrl.SetLabel(self.valueLabel % {"1": value})
        else:
            self.valueLabelCtrl.SetLabel(self.levelCallback(value))
        if dummyEvent:
            dummyEvent.Skip()

    def OnSetFocus(self, dummyEvent):
        self.slider.SetFocus()

    def OnSize(self, dummyEvent):
        if self.GetAutoLayout():
            self.Layout()

    def SetValue(self, value):
        self.slider.SetValue(value)
        self.OnScrollChanged()
