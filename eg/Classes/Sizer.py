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
import types


class Sizer(wx.PySizer):
    
    def __init__(self, parent, vgap=0, hgap=0):
        wx.PySizer.__init__(self)
        self.parent = parent
        self.vgap = vgap
        self.hgap = hgap
        self.row = 0
        
        
    def AddLine(self, *items, **kwargs):
        flag = wx.ALIGN_CENTER_VERTICAL
        for col, item in enumerate(items):
            if type(item) in types.StringTypes:
                item = wx.StaticText(self.parent, -1, item)
            self.Add(item, 0, flag, 0, userData=(self.row, col))
        self.row += 1
        
    
    def CalcMin(self):
        return wx.Size(100, 100)
    
    
    def RecalcSizes(self):
        curWidth, curHeight = self.GetSize()
        px, py = self.GetPosition()
        x, y = 0, 0
        maxItemHeight = 0
        for item in self.GetChildren():
            row, col = item.GetUserData()
            w, h = item.CalcMin()
            maxItemHeight = max(maxItemHeight, h)
        
            print row, col, item.CalcMin()
            
    
    
        