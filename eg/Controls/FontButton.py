# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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


class FontButton(wx.Button):
    
    def __init__(
        self, 
        parent, 
        id=-1,
        label="Font", 
        pos=wx.DefaultPosition, 
        size=wx.DefaultSize, 
        style=0, 
        validator=wx.DefaultValidator, 
        name="font button", 
        fontInfo=None
    ):
        self.fontInfo = fontInfo
        wx.Button.__init__(
            self, 
            parent, 
            id, 
            label, 
            pos, 
            size, 
            style,
            validator, 
            name
        )
        self.Bind(wx.EVT_BUTTON, self.OnFontButton)
        
        
    def OnFontButton(self, event):
        data = wx.FontData()
        if self.fontInfo is not None:
            font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
            nfi = wx.NativeFontInfo()
            nfi.FromString(self.fontInfo)
            font.SetNativeFontInfo(nfi)
            data.SetInitialFont(font)
        dlg = wx.FontDialog(self.GetParent(), data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.fontInfo = font.GetNativeFontInfo().ToString()
        dlg.Destroy()       
        
        
    def GetValue(self):
        return self.fontInfo
    
    