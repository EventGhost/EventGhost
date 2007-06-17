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


class Dialog(wx.Dialog):
    __instance = None
    
    @classmethod
    def ShowModeless(cls, *args, **kwargs):
        self = cls.__instance
        if self:
            self.Show()
            self.Raise()
            return self
        else:
            self = cls(*args, **kwargs)
            @eg.LogIt
            def OnDestroy(event):
                cls.__instance = None
                event.Skip()
            self.Bind(wx.EVT_WINDOW_DESTROY, OnDestroy)
            @eg.LogIt
            def OnClose(event):
                self.Destroy()
                event.Skip()
            self.Bind(wx.EVT_CLOSE, OnClose)

            cls.__instance = self
            self.Show()
            return self
    
        
    def DoModal(self):
        result = None
        if self.ShowModal() == wx.ID_OK and hasattr(self, "resultData"):
            result = self.resultData
        self.Destroy()
        return result
    
    
        
