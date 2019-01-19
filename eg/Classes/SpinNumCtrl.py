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
from wx.lib import masked

import eg

THOUSANDS_SEP = eg.app.locale.GetInfo(wx.LOCALE_THOUSANDS_SEP)
DECIMAL_POINT = eg.app.locale.GetInfo(wx.LOCALE_DECIMAL_POINT)


class SpinNumError(ValueError):
    _msg = ''

    def __init__(self, *args):
        if args:
            self._msg = self._msg.format(*args)

    def __str__(self):
        return self._msg


class MinValueError(SpinNumError):
    _msg = 'The set value {0} is lower then the minimum of {1}'


class MaxValueError(SpinNumError):
    _msg = 'The set value {0} is higher then the maximum of {1}'


class MinMaxValueError(SpinNumError):
    _msg = 'The minimum value {0} is higher the the max value {0}.'


class NegativeValueError(SpinNumError):
    _msg = 'The minimum value needs to be set when using negative values.'


class SpinNumCtrl(wx.Window):
    """
    A wx.Control that shows a fixed width floating point value and spin
    buttons to let the user easily input a floating point value.
    """
    _defaultArgs = {
        "integerWidth": 3,
        "fractionWidth": 2,
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

        self.increment = kwargs.pop("increment", 1)
        min_val = kwargs.pop('min', None)
        max_val = kwargs.pop('max', None)
        allow_negative = kwargs.pop("allowNegative", False)

        tmp = self._defaultArgs.copy()
        tmp.update(kwargs)
        kwargs = tmp

        if max_val is None and min_val is None:
            if value < 0:
                raise NegativeValueError

        elif min_val is None and max_val is not None:
            if value > max_val:
                raise MaxValueError(value, max_val)
            if max_val < 0:
                allow_negative = True

        elif max_val is None and min_val is not None:
            if value < min_val:
                raise MinValueError(value, min_val)
            if min_val < 0:
                allow_negative = True

        else:
            if min_val > max_val:
                raise MinMaxValueError(min_val, max_val)
            if value < min_val:
                raise MinValueError(value, min_val)
            if value > max_val:
                raise MaxValueError(value, max_val)
            if min_val < 0:
                allow_negative = True

        if max_val is None:
            max_val = (
                (10 ** kwargs["integerWidth"]) -
                (10 ** -kwargs["fractionWidth"])
            )

        wx.Window.__init__(self, parent, id, pos, size, 0)
        self.SetThemeEnabled(True)
        numCtrl = masked.NumCtrl(
            self,
            -1,
            value,
            pos,
            size,
            style,
            validator,
            name,
            allowNone=True,
            allowNegative=allow_negative,
            min=min_val,
            max=max_val,
            **kwargs
        )
        self.numCtrl = numCtrl

        numCtrl.SetCtrlParameters(
            validBackgroundColour=wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW),
            emptyBackgroundColour=wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW),
            foregroundColour=wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT),
        )

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
        if value < 0 and not self.numCtrl.IsNegativeAllowed():
            value = 0
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
