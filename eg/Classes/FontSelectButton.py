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


class FontSelectButton(wx.BitmapButton):
    
    def __init__(
        self, 
        parent, 
        id=-1,
        pos=wx.DefaultPosition, 
        size=(40, wx.Button.GetDefaultSize()[1]), 
        style=wx.BU_AUTODRAW, 
        validator=wx.DefaultValidator, 
        name="FontSelectButton", 
        fontInfo=None
    ):
        self.fontInfo = fontInfo
        wx.BitmapButton.__init__(
            self, 
            parent, 
            id, 
            wx.Bitmap("images/font.png"), 
            pos, 
            size, 
            style,
            validator, 
            name
        )
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        
        
    def OnButton(self, event):
        data = wx.FontData()
        if self.fontInfo is not None:
            font = wx.FontFromNativeInfoString(self.fontInfo)  
            data.SetInitialFont(font)
        else:
            data.SetInitialFont(
                wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT)
            )
        dlg = wx.FontDialog(self.GetParent(), data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.fontInfo = font.GetNativeFontInfo().ToString()
            event.Skip()
        dlg.Destroy()       
        
        
    def GetValue(self):
        return self.fontInfo
    
    
    def SetValue(self, fontInfo):
        self.fontInfo = fontInfo

