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
        value=None
    ):
        self.value = value
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
        fontData = wx.FontData()
        if self.value is not None:
            font = wx.FontFromNativeInfoString(self.value)  
            fontData.SetInitialFont(font)
        else:
            fontData.SetInitialFont(
                wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT)
            )
        dialog = wx.FontDialog(self.GetParent(), fontData)
        if dialog.ShowModal() == wx.ID_OK:
            fontData = dialog.GetFontData()
            font = fontData.GetChosenFont()
            self.value = font.GetNativeFontInfo().ToString()
            event.Skip()
        dialog.Destroy()       
        
        
    def GetValue(self):
        return self.value
    
    
    def SetValue(self, value):
        self.value = value

