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


PROMPT = "Please type your input..."

class SimpleInputDialog(eg.Dialog):
    
    def __init__(self, prompt=None, initialValue=""):
        if prompt is None:
            prompt = PROMPT
        eg.Dialog.__init__(
            self, None, -1, PROMPT, style=wx.RESIZE_BORDER|wx.CAPTION
        )
        textCtrl = self.TextCtrl(initialValue, size=(300, -1))
        buttonRow = eg.ButtonRow(self, [wx.ID_OK])
        mainSizer = eg.VBoxSizer(
            (self.StaticText(prompt), 0, wx.EXPAND|wx.ALL, 5),
            (textCtrl, 0, wx.EXPAND|wx.ALL, 5),
            ((5, 5), 1, wx.EXPAND),
            (wx.StaticLine(self), 0, wx.EXPAND),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(mainSizer)
        self.SetMinSize(self.GetSize())
        while self.Affirmed():
            self.SetResult(textCtrl.GetValue())
        
        
    @classmethod
    def CreateModal(cls, prompt=None):
        return cls.GetModalResult(prompt)
    
    