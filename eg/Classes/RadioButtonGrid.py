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
# $LastChangedDate: 2007-03-18 13:14:34 +0100 (So, 18 Mrz 2007) $
# $LastChangedRevision: 81 $
# $LastChangedBy: bitmonster $


class RadioButtonGrid(wx.Panel):
    CtrlType = wx.RadioButton
    firstCtrlStyle = wx.RB_GROUP
    
    def __init__(
        self, 
        parent, 
        id = wx.ID_ANY, 
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        rows = None, 
        columns = None
    ):
        wx.Panel.__init__(self, parent, id, pos, size)
        biggestWidth = 0
        sizer = wx.FlexGridSizer(len(rows) + 2, len(columns) + 1)
        sizer.Add((0, 0))
        for column in columns:
            staticText = wx.StaticText(self, -1, column)
            width, height = staticText.GetBestSize()
            if width > biggestWidth:
                biggestWidth = width
            sizer.Add(staticText, 0, wx.ALIGN_CENTER_HORIZONTAL)
                
        self.ctrlTable = ctrlTable = []
        for column in columns:
            ctrl = self.CtrlType(self, style=self.firstCtrlStyle)
            ctrlColumn = [ctrl]
            for row in rows[1:]:
                ctrl = self.CtrlType(self)
                ctrlColumn.append(ctrl)
            ctrlTable.append(ctrlColumn)

        biggestWidth += 3
        width, height= ctrl.GetBestSize()
        if width > biggestWidth:
            biggestWidth = width

        for y, row in enumerate(rows):
            staticText = wx.StaticText(self, -1, row)
            sizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL)
            for x, column in enumerate(columns):
                ctrl = ctrlTable[x][y]
                sizer.Add(ctrl, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        sizer.Add((0, 0))
        for column in columns:
            sizer.Add((biggestWidth, 0))

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        
    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()


    def GetValue(self):
        result = []
        for column in self.ctrlTable:
            for i, ctrl in enumerate(column):
                if ctrl.GetValue():
                    break
            result.append(i)
        return result
            
            
    def SetValue(self, value):
        for column, val in enumerate(value):
            self.ctrlTable[column][val].SetValue(True)
            
            
            