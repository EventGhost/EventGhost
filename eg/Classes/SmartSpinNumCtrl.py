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

class SmartSpinNumCtrl(wx.Window):
    """
    A wx.Control that shows a fixed width floating point value and spin
    buttons to let the user easily input a floating point value.
    """
    ctrl = None

    def __init__(
        self,
        parent,
        id=-1,
        value=0.0,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TE_RIGHT,
        validator=wx.DefaultValidator,
        name="eg.SmartSpinNumCtrl",
        **kwargs
    ):
        self.initValue = 0.0
        self.value = value
        self.parent = parent
        self.kwargs = kwargs
        self.name = name
        self.nW = size[0] if size[0] != -1 else 60
        self.tW = size[0] if size[0] != -1 else 120
        if 'numWidth' in self.kwargs:
            self.nW = self.kwargs['numWidth']
            del self.kwargs['numWidth']
        if 'textWidth' in self.kwargs:
            self.tW = self.kwargs['textWidth']
            del self.kwargs['textWidth']

        wx.Window.__init__(self, parent, id, pos, size, 0)
        self.SetThemeEnabled(True)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.ctrl = self.CreateCtrl(int(not isinstance(value, (int, float))))
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def CreateCtrl(self, ctrlType, init = True):
        szr = self.sizer
        szr.Clear(True)
        if ctrlType == 0:
            ctrl = eg.SpinNumCtrl(
                self,
                -1,
                self.initValue,
                **self.kwargs
            )
            ctrl.numCtrl.Bind(wx.EVT_RIGHT_UP, self.OnRclick)
            ctrl.numCtrl.SetToolTipString(eg.text.General.smartSpinTooltip)
            if init:
                ctrl.SetValue(self.value)
        else:
            ctrl = wx.TextCtrl(
                self,
                -1,
                str(self.value),
            )
            ctrl.Bind(wx.EVT_RIGHT_UP, self.OnRclick)
            ctrl.SetToolTipString(eg.text.General.smartSpinTooltip)
            if not init:
                ctrl.SetValue(("", "{eg.result}", "{eg.event.payload}", "")[ctrlType])
        szr.Add(ctrl, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        szr.Layout()
        self.UpdateWidth(ctrl)
        return ctrl

    def GetSize(self):
        return self.ctrl.GetSize()

    def GetValue(self):
        return self.ctrl.GetValue()

    def OnMenu(self, evt):
        self.ctrl = self.CreateCtrl(self.popups.index(evt.GetId()), False)

    def OnRclick(self, evt):
        if not hasattr(self, "popupId0"):
            self.popupId0 = wx.NewId()
            self.popupId1 = wx.NewId()
            self.popupId2 = wx.NewId()
            self.popupId3 = wx.NewId()
            self.popups = (
                self.popupId0,
                self.popupId1,
                self.popupId2,
                self.popupId3
            )
            self.Bind(wx.EVT_MENU, self.OnMenu, id=self.popupId0)
            self.Bind(wx.EVT_MENU, self.OnMenu, id=self.popupId1)
            self.Bind(wx.EVT_MENU, self.OnMenu, id=self.popupId2)
            self.Bind(wx.EVT_MENU, self.OnMenu, id=self.popupId3)
        menu = wx.Menu()
        for i in range(4):
            menu.Append(self.popups[i], eg.text.General.smartSpinMenu[i])
        self.PopupMenu(menu)
        menu.Destroy()

    def OnSize(self, dummyEvent):
        if self.GetAutoLayout():
            self.Layout()

    def SetSize(self, size):
        w = size[0]
        if w != -1:
            self.tW = w
            self.nW = w
        self.UpdateWidth(self.ctrl)

    def SetValue(self, value):
        if isinstance(self.ctrl, eg.Classes.SpinNumCtrl.SpinNumCtrl):
            if isinstance(value, (str, unicode)):
                value = float(value)
            minValue, maxValue = self.ctrl.numCtrl.GetBounds()
            if maxValue is not None and value > maxValue:
                value = maxValue
            if minValue is not None and value < minValue:
                value = minValue
        elif isinstance(value, (int, float)):
            value = str(value)
        res = self.ctrl.SetValue(value)
        wx.PostEvent(self, eg.ValueChangedEvent(self.GetId(), value = value))
        return res

    def UpdateWidth(self, ctrl):
        w = (self.tW, self.nW)[int(isinstance(ctrl, eg.Classes.SpinNumCtrl.SpinNumCtrl))]
        parentSizer = self.GetContainingSizer()
        if parentSizer:
            parentSizer.SetItemMinSize(self, w, -1)
            parentSizer.Layout()
        else:
            ctrl.SetMinSize((w, -1))
            ctrl.SetSize((w, -1))
