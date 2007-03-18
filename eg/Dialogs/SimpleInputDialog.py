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

import sys
import threading
import wx
import eg


PROMPT = "Please type your input..."

class SimpleInputDialog(wx.Dialog):
    def __init__(self, prompt="", initial_value=""):
        self.result = None
        wx.Dialog.__init__(
            self, None, -1, PROMPT, style=wx.RESIZE_BORDER|wx.CAPTION
        )
        st = wx.StaticText(self, -1, prompt)
        self.textCtrl = wx.TextCtrl(self, -1, initial_value, size=(300,-1))
        btnrow = eg.ButtonRow(self, [wx.ID_OK])
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(st, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.textCtrl, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add((5,5), 1, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        mainSizer.Add(btnrow.sizer, 0, wx.EXPAND)        
        self.SetSizerAndFit(mainSizer)
        self.SetMinSize(self.GetSize())
        
        
    def OnOK(self, event):
        self.result = self.textCtrl.GetValue()
        event.Skip()
        
        
        
def ShowSimpleRawDialog(event, result_list, prompt=PROMPT):
    dialog = SimpleInputDialog(prompt)
    dialog.ShowModal()
    result_list[0] = dialog.result
    dialog.Destroy()
    event.set()
    
import pythoncom

def GetSimpleRawInput(prompt=PROMPT):
    event = threading.Event()
    result_list = [None]
    wx.CallAfter(ShowSimpleRawDialog, event, result_list, prompt)
    while not event.isSet():
        pythoncom.PumpWaitingMessages()
    #event.wait()
    return result_list[0]


def GetSimpleInput(prompt=PROMPT):
    return eval(GetSimpleRawInput(prompt))

    
