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

import eg
import wx


class StatusBar(wx.StatusBar):
    
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-1, 40])
        self.icons = [
            eg.Icons.GetIcon("images\\Tray1.png"),
            eg.Icons.GetIcon("images\\Tray3.png"),
            eg.Icons.GetIcon("images\\Tray2.png"),
        ]
        self.icon = wx.StaticBitmap(self, -1, self.icons[0], (0, 0), (16, 16))
        rect = self.GetFieldRect(0)
        checkBox = wx.CheckBox(self, -1, eg.text.MainFrame.onlyLogAssigned)
        self.checkBox = checkBox
        colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_MENUBAR)
        checkBox.SetBackgroundColour(colour)
        self.checkBoxColour = checkBox.GetForegroundColour()
        checkBox.SetValue(eg.config.onlyLogAssigned)
        self.SetCheckBoxColour(eg.config.onlyLogAssigned)
        checkBox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        checkBox.SetPosition((rect.x + 2, rect.y + 2))
        checkBox.SetToolTipString(eg.text.MainFrame.onlyLogAssignedToolTip)
        eg.Bind("ProcessingChange", self.OnProcessingChange)
        self.Reposition()


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
    
    
    @eg.LogIt
    def Destroy(self):
        eg.Unbind("ProcessingChange", self.OnProcessingChange)
        return wx.StatusBar.Destroy(self)

    
    def OnSize(self, dummyEvent):
        self.Reposition()  # for normal size events
        self.sizeChanged = True


    def OnIdle(self, dummyEvent):
        if self.sizeChanged:
            self.Reposition()


    def Reposition(self):
        rect = self.GetFieldRect(1)
        y = rect.y + (rect.height - 16) / 2
        self.icon.SetPosition((rect.x + 5, y))
        self.sizeChanged = False
                
        
    def SetCheckBoxColour(self, value):
        if value:
            self.checkBox.SetForegroundColour((255, 0, 0))
        else:
            self.checkBox.SetForegroundColour(self.checkBoxColour)
        
    
    @eg.LogIt
    def OnCheckBox(self, dummyEvent):
        eg.config.onlyLogAssigned = self.checkBox.GetValue()
        self.SetCheckBoxColour(eg.config.onlyLogAssigned)
        
        
    def OnProcessingChange(self, state):
        self.icon.SetBitmap(self.icons[state])
            
