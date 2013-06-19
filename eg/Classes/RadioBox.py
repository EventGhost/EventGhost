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

import wx


class RadioBox(wx.Panel):
    
    def __init__(
        self,
        parent = None,
        id = -1,
        label = "",
        pos = (-1, -1),
        size = (-1, -1),
        choices = (),
        majorDimension = 0,
        style = wx.RA_SPECIFY_COLS,
        validator = wx.DefaultValidator,
        name = "radioBox"
    ):
        self.value = 0
        wx.Panel.__init__(self, parent, id, pos, size, name=name)
        sizer = self.sizer = wx.GridSizer(len(choices), 1, 6, 6)
        style = wx.RB_GROUP
        for i, choice in enumerate(choices):
            radioButton = wx.RadioButton(self, i, choice, style=style)
            style = 0
            self.sizer.Add(radioButton, 0, wx.EXPAND)
            radioButton.Bind(wx.EVT_RADIOBUTTON, self.OnSelect)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

    
    def OnSelect(self, event):
        self.value = event.GetId()
        newEvent = wx.CommandEvent(wx.EVT_RADIOBOX.evtType[0], self.GetId())
        newEvent.SetInt(self.value)
        self.ProcessEvent(newEvent)
        
        
    def SetSelection(self, selection):
        self.FindWindowById(selection).SetValue(True)
        self.value = selection
    
    
    def GetSelection(self):
        return self.value
    
    
    def GetValue(self):
        return self.value
    
    
    def SetValue(self, value):
        self.SetSelection(int(value))
    
