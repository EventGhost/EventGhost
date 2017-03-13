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
from wx import SystemSettings_GetColour as GetColour
from wx.lib import masked

import eg

l = wx.Locale()
l.Init2(language=wx.LANGUAGE_DEFAULT, flags=wx.LOCALE_LOAD_DEFAULT)
THOUSANDS_SEP = l.GetInfo(wx.LOCALE_THOUSANDS_SEP)
DECIMAL_POINT = l.GetInfo(wx.LOCALE_DECIMAL_POINT)


class SpinNumCtrl(wx.Window):
    """
    A wx.Control that shows a fixed width floating point value and spin
    buttons to let the user easily input a floating point value.
    """
    _defaultArgs = {
        "integerWidth": 3,
        "fractionWidth": 2,
        "allowNegative": False,
        "min": 0,
        "limited": True,
        "groupChar": THOUSANDS_SEP,
        "decimalChar": DECIMAL_POINT,
    }

    def __init__(
        self,
        parent,
        id=-1,
        value=0.0,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TE_RIGHT,
        validator=wx.DefaultValidator,
        name="eg.SpinNumCtrl",
        **kwargs
    ):
        if "increment" in kwargs:
            self.increment = kwargs.pop("increment")
        else:
            self.increment = 1

        tmp = self._defaultArgs.copy()
        tmp.update(kwargs)
        kwargs = tmp

        if kwargs['min'] < 0:
            kwargs["allowNegative"] = True
        if "max" not in kwargs:
            kwargs["max"] = (
                (10 ** kwargs["integerWidth"]) -
                (10 ** -kwargs["fractionWidth"])
            )
        wx.Window.__init__(self, parent, id, pos, size, 0)
        self.SetThemeEnabled(True)
        numCtrl = masked.NumCtrl(
            self,
            -1,
            0, # Can't set value here, to avoid bug in NumCtrl
            pos,
            size,
            style,
            validator,
            name,
            allowNone=True,
            # **kwargs # Can't set kwargs here, to avoid bug in NumCtrl
        )
        numCtrl.SetParameters(**kwargs)  # To avoid bug in NumCtrl
        numCtrl.SetValue(value)  # To avoid bug in NumCtrl

        self.numCtrl = numCtrl
        numCtrl.SetCtrlParameters(
            validBackgroundColour=GetColour(wx.SYS_COLOUR_WINDOW),
            emptyBackgroundColour=GetColour(wx.SYS_COLOUR_WINDOW),
            foregroundColour=GetColour(wx.SYS_COLOUR_WINDOWTEXT),
        )
        numCtrl.SetLimited(True)
        height = numCtrl.GetSize()[1]
        spinbutton = wx.SpinButton(
            self,
            -1,
            style=wx.SP_VERTICAL,
            size=(height * 2 / 3, height)
        )
        spinbutton.MoveBeforeInTabOrder(numCtrl)
        self.spinbutton = spinbutton
        numCtrl.Bind(wx.EVT_CHAR, self.OnChar)
        spinbutton.Bind(wx.EVT_SPIN_UP, self.OnSpinUp)
        spinbutton.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown)

        sizer = self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(numCtrl, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        sizer.Add(spinbutton, 0, wx.ALIGN_CENTER)
        self.SetSizerAndFit(sizer)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        wx.CallAfter(numCtrl.SetSelection, -1, -1)

    def GetValue(self):
        return self.numCtrl.GetValue()

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_UP:
            self.OnSpinUp(event)
            return
        if key == wx.WXK_DOWN:
            self.OnSpinDown(event)
            return
        event.Skip()

    def OnSetFocus(self, dummyEvent):
        self.numCtrl.SetFocus()
        self.numCtrl.SetSelection(-1, -1)

    def OnSize(self, dummyEvent):
        if self.GetAutoLayout():
            self.Layout()

    def OnSpinDown(self, dummyEvent):
        value = self.numCtrl.GetValue() - self.increment
        self.SetValue(value)

    def OnSpinUp(self, dummyEvent):
        value = self.numCtrl.GetValue() + self.increment
        self.SetValue(value)

    def SetValue(self, value):
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        res = self.numCtrl.SetValue(value)
        wx.PostEvent(self, eg.ValueChangedEvent(self.GetId(), value=value))
        return res

    def __OnSpin(self, pos):
        """
        This is the function that gets called in response to up/down arrow or
        bound spin button events.
        """

        # Ensure adjusted control regains focus and has adjusted portion
        # selected:
        numCtrl = self.numCtrl
        numCtrl.SetFocus()
        start, end = numCtrl._FindField(pos)._extent
        numCtrl.SetInsertionPoint(start)
        numCtrl.SetSelection(start, end)
