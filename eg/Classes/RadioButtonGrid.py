# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import wx

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
            width = staticText.GetBestSize()[0]
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
        width = ctrl.GetBestSize()[0]
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

    def GetValue(self):
        result = []
        for column in self.ctrlTable:
            for i, ctrl in enumerate(column):
                if ctrl.GetValue():
                    break
            result.append(i)
        return result

    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

    def SetValue(self, value):
        for column, val in enumerate(value):
            self.ctrlTable[column][val].SetValue(True)
