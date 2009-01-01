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

STANDARD_IDS = (wx.ID_OK, wx.ID_CANCEL, wx.ID_APPLY, wx.ID_HELP)


class ButtonRow(object):
    
    def __init__(self, parent, buttonIds, resizeGrip=False):
        self.parent = parent
        self.numSpecialCtrls = 0
        self.stdbtnsizer = stdbtnsizer = wx.StdDialogButtonSizer()
        defaultButton = None
        text = eg.text.General
        for ctrl in buttonIds:
            if ctrl not in STANDARD_IDS:
                stdbtnsizer.Add(ctrl)
                
        if wx.ID_OK in buttonIds:
            okButton = wx.Button(parent, wx.ID_OK, text.ok)
            okButton.Bind(wx.EVT_BUTTON, self.OnOK)
            stdbtnsizer.AddButton(okButton)
            defaultButton = okButton
            self.okButton = okButton
            
        if wx.ID_CANCEL in buttonIds:
            cancelButton = wx.Button(parent, wx.ID_CANCEL, text.cancel)
            cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
            stdbtnsizer.AddButton(cancelButton)
            if not defaultButton:
                defaultButton = cancelButton
            self.cancelButton = cancelButton
        
        if wx.ID_APPLY in buttonIds:
            applyButton = wx.Button(parent, wx.ID_APPLY, text.apply)
            applyButton.Bind(wx.EVT_BUTTON, self.OnApply)
            stdbtnsizer.AddButton(applyButton)
            if not defaultButton:
                defaultButton = applyButton
            self.applyButton = applyButton
        
        if wx.ID_HELP in buttonIds:
            helpButton = wx.Button(parent, wx.ID_HELP, text.help)
            helpButton.Bind(wx.EVT_BUTTON, self.OnHelp)
            stdbtnsizer.AddButton(helpButton)
            if not defaultButton:
                defaultButton = helpButton
            self.helpButton = helpButton
        
        stdbtnsizer.Realize()
        defaultButton.SetDefault()
        
        self.sizer = sizer = wx.BoxSizer(wx.HORIZONTAL)
        if resizeGrip:
            self.sizeGrip = eg.SizeGrip(parent)
            sizer.Add(self.sizeGrip.GetSize(), 1)
            sizer.Add(stdbtnsizer, 0, wx.TOP|wx.BOTTOM, 6)
            sizer.Add(self.sizeGrip, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)
        else:
            sizer.Add((3, 3), 1)
            sizer.Add(stdbtnsizer, 0, wx.TOP|wx.BOTTOM, 6)
            sizer.Add((2, 2), 0)      
        
        
    def Add(
        self, 
        ctrl, 
        proportion=0, 
        flags=wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 
        border=5
    ):
        if self.numSpecialCtrls == 0:
            self.sizer.Insert(0, (15, 5))
        self.sizer.Insert(
            self.numSpecialCtrls+1, 
            ctrl, 
            proportion, 
            flags, 
            border
        )
        self.numSpecialCtrls += 1
        
    
    def OnOK(self, event):
        if hasattr(self.parent, "OnOK"):
            self.parent.OnOK(event)
        else:
            event.Skip()
            
            
    def OnCancel(self, event):
        if hasattr(self.parent, "OnCancel"):
            self.parent.OnCancel(event)
        else:
            event.Skip()
            
            
    def OnApply(self, event):
        if hasattr(self.parent, "OnApply"):
            self.parent.OnApply(event)
        else:
            event.Skip()
            
            
    def OnHelp(self, event):
        if hasattr(self.parent, "OnHelp"):
            self.parent.OnHelp(event)
        else:
            event.Skip()

