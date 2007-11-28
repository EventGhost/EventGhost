# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import locale
import wx
from wx.lib import masked


encoding = locale.getdefaultlocale()[1]
localedict = locale.localeconv()


class SpinNumCtrl(wx.Window):
    """A wx.Control that shows a fixed width floating point value and spin 
    buttons to let the user change it.
    """
    
    EVT_NUM = masked.EVT_NUM
    _defaultArgs = {
        "integerWidth": 3,
        "fractionWidth": 2,
        "allowNegative": False,
        "min": 0,
        "limited": True,
        "groupChar": localedict['thousands_sep'].decode(encoding),
        "decimalChar": localedict['decimal_point'].decode(encoding),
    }
    
    def __init__(
        self, 
        parent, 
        id=-1,
        value = 0.0,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = wx.TE_RIGHT,
        validator = wx.DefaultValidator,
        name = "eg.SpinNumCtrl", 
        **kwargs
    ):
        if kwargs.has_key("increment"):
            self.increment = kwargs["increment"]
            del kwargs["increment"]
        else:
            self.increment = 1

        newArgs = self._defaultArgs.copy()
        if kwargs.has_key("min"):
            if kwargs["min"] < 0:
                newArgs["allowNegative"] = True
                
        newArgs.update(kwargs)
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
            #**newArgs # to avoid bug in NumCtrl
        )
        numCtrl.SetParameters(**newArgs) # to avoid bug in NumCtrl
        
        self.numCtrl = numCtrl
        numCtrl.SetCtrlParameters(        
            validBackgroundColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW),
            emptyBackgroundColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW),
            foregroundColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT),
        )
        numCtrl.SetLimited(True)
        w, h = numCtrl.GetSize()
        spinbutton = wx.SpinButton(
            self, 
            -1, 
            style=wx.SP_VERTICAL,
            size=(h*2/3, h)
        )
        spinbutton.MoveBeforeInTabOrder(numCtrl)
        self.spinbutton = spinbutton
        numCtrl.Bind(wx.EVT_CHAR, self.OnChar)
        spinbutton.Bind(wx.EVT_SPIN_UP, self.OnSpinUp)
        spinbutton.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(numCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        sizer.Add(spinbutton, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        wx.CallAfter(numCtrl.SetSelection, -1, -1)
        

    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()


    def OnSetFocus(self, event):
        self.numCtrl.SetFocus()
        self.numCtrl.SetSelection(-1, -1)
        
        
    def OnSpinUp(self, event):
        value = self.numCtrl.GetValue() + self.increment
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        self.numCtrl.SetValue(value)
        
        
    def OnSpinDown(self, event):
        value = self.numCtrl.GetValue() - self.increment
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        self.numCtrl.SetValue(value)
    
    
    def OnChar(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_UP:
            self.OnSpinUp(event)
            return
        if key == wx.WXK_DOWN:
            self.OnSpinDown(event)
            return
        event.Skip()
        
        
    def GetValue(self):
        return self.numCtrl.GetValue()


    def SetValue(self, value):
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        return self.numCtrl.SetValue(value)



