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
import eg


class BrowseMacroButton(wx.Window):
    
    def __init__(self, parent, label, title, mesg, macro=None):
        if macro is None:
            macro_name = ""
        else:
            macro_name = macro.name
        self.title = title
        self.mesg = mesg
        self.macro = macro
        wx.Window.__init__(self, parent, -1)
        self.textBox = eg.StaticTextBox(self, -1, macro_name, size=(200,-1))
        self.button = wx.Button(self, -1, label)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.textBox, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.button, 0, wx.LEFT, 5)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Layout()


    def OnSetFocus(self, event):
        self.button.SetFocus()
        
        
    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

        
    def OnButton(self, event):
        macro = eg.TreeItemBrowseDialog(
            self.title,
            self.mesg, 
            self.macro, 
            (eg.MacroItem,)
        ).DoModal()
        if macro:
            self.textBox.SetLabel(macro.name)
            self.macro = macro
            
            
    def GetValue(self):
        return self.macro
