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

PROMPT = "Please type your input..."

class SimpleInputDialog(eg.Dialog):
    def __init__(self, prompt=None, initialValue=""):
        if prompt is None:
            prompt = PROMPT
        self.resultData = None
        wx.Dialog.__init__(
            self, None, -1, PROMPT, style=wx.RESIZE_BORDER|wx.CAPTION
        )
        st = wx.StaticText(self, -1, prompt)
        self.textCtrl = wx.TextCtrl(self, -1, initialValue, size=(300, -1))
        btnrow = eg.ButtonRow(self, [wx.ID_OK])
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(st, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.textCtrl, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add((5, 5), 1, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        mainSizer.Add(btnrow.sizer, 0, wx.EXPAND)        
        self.SetSizerAndFit(mainSizer)
        self.SetMinSize(self.GetSize())
        
        
    def OnOK(self, event):
        self.resultData = self.textCtrl.GetValue()
        event.Skip()
                
        
    @classmethod
    def CreateModal(cls, prompt=None):
        return cls(prompt).DoModal()