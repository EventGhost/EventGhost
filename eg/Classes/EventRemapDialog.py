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
# $LastChangedDate: 2007-10-05 02:25:25 +0200 (Fri, 05 Oct 2007) $
# $LastChangedRevision: 242 $
# $LastChangedBy: bitmonster $

import eg
import wx


class EventRemapDialog(eg.Dialog):
    
    def __init__(self, parent, mapping=None):
        
        eg.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        listCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        listCtrl.InsertColumn(0, "New event name")
        listCtrl.InsertColumn(1, "Events")
        listCtrl.InsertColumn(2, "Repeat events")
        listCtrl.InsertColumn(3, "Timeout")
        
        newEventCtrl = wx.TextCtrl(self, -1)
        eventsCtrl = wx.TextCtrl(self, -1)
        repeatEventsCtrl = wx.TextCtrl(self, -1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(listCtrl, 1, wx.EXPAND)
        
        editSizer = wx.GridSizer(1, 2)
        editSizer.Add(wx.StaticText(self, -1, "New event name:"), wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(newEventCtrl, 0)
        editSizer.Add(wx.StaticText(self, -1, "Events:"), wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(eventsCtrl, 0)
        editSizer.Add(wx.StaticText(self, -1, "Repeat events:"), wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(repeatEventsCtrl, 0)
        
        sizer.Add(editSizer)
        self.SetSizerAndFit(sizer)
        
        
        
        
