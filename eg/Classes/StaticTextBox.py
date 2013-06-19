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


class StaticTextBox(wx.PyWindow):
    
    def __init__(self, parent, id=-1, label='', pos=(-1,-1), size=(-1,-1)):
        wx.Window.__init__(
            self, 
            parent, 
            id, 
            pos, 
            size,
            style=wx.SUNKEN_BORDER
        )
        self.SetMinSize(self.GetSize())
        sizer = wx.BoxSizer(wx.VERTICAL)
        textCtrl = wx.StaticText(self, -1, label)
        sizer.Add((0,0), 1, wx.EXPAND)
        sizer.Add(textCtrl, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        sizer.Add((0,0), 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.textCtrl = textCtrl


    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()


    def SetLabel(self, label):
        self.textCtrl.SetLabel(label)


    def AcceptsFocus(self):
        return False
    
