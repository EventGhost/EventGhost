## -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
# 
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx
import types


class ConfigPanel(wx.PyPanel, eg.ControlProviderMixin):
    """
    A panel with some magic.
    """

    def __init__(
        self,
        executable=None,
        resizable=None,
        showLine=True
    ):
        #if resizable is None:
        #    resizable = bool(eg.debugLevel)
        item = eg.currentConfigureItem

        dialog = item.openConfigDialog
        dialog.panel = self
        dialog.__init__(item, resizable, showLine)
        self.dialog = dialog
        wx.PyPanel.__init__(self, dialog)
        self.lines = []
        dialog.sizer.Add(self, 1, wx.EXPAND)
        self.sizerProps = (6, 5)
        self.rowFlags = {}
        self.colFlags = {}
        self.shown = False
        self.maxRowNum = 0
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.isDirty = False
        self.resultCode = None
        self.buttonsEnabled = True
        self.dialog.buttonRow.applyButton.Enable(False)


    @eg.LogIt
    def SetIsDirty(self, flag=True):
        self.isDirty = flag
        if flag and self.buttonsEnabled:
            self.dialog.buttonRow.applyButton.Enable(True)


    def AddLabel(self, label):
        self.sizer.Add(self.StaticText(label), 0, wx.BOTTOM, 2)


    def AddCtrl(self, ctrl):
        self.sizer.Add(ctrl, 0, wx.BOTTOM, 10)


    def SetSizerProperty(self, vgap=6, hgap=5):
        self.sizerProps = (vgap, hgap)


    def SetRowFlags(self, rowNum, flags):
        self.rowFlags[rowNum] = flags


    def SetColumnFlags(self, colNum, flags):
        self.colFlags[colNum] = flags


    def FinishSetup(self):
        self.shown = True
        if self.lines:
            self.AddGrid(self.lines, *self.sizerProps)
        else:
            self.SetSizerAndFit(self.sizer)

        #self.dialog.FinishSetup()
        def OnEvent(dummyEvent):
            self.SetIsDirty()
        self.Bind(wx.EVT_CHECKBOX, OnEvent)
        self.Bind(wx.EVT_BUTTON, OnEvent)
        self.Bind(wx.EVT_CHOICE, OnEvent)
        self.Bind(wx.EVT_TOGGLEBUTTON, OnEvent)
        self.Bind(wx.EVT_TEXT, OnEvent)
        self.Bind(wx.EVT_RADIOBOX, OnEvent)
        self.Bind(wx.EVT_RADIOBUTTON, OnEvent)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, OnEvent)
        self.Bind(wx.EVT_DATE_CHANGED, OnEvent)
        self.Bind(eg.EVT_VALUE_CHANGED, OnEvent)
        self.Bind(wx.EVT_CHECKLISTBOX, OnEvent)


    def Affirmed(self):
        """
        Returns the user request.

        If called the first time, it will also finish creation of the panel
        and show it to the user, before returning the user request.

        The return value depends on the button the user has pressed in the
        panel:

            | Cancel button => :const:`False`
            | Ok button => :const:`wx.ID_OK`
            | Apply button => :const:`wx.ID_APPLY`
            | Test button => :const:`eg.ID_TEST`
        """
        self.resultCode = self.dialog.Affirmed()
        return self.resultCode


    def SetResult(self, *args):
        """
        Notifies the program of the current values of the configuration
        controls.
        """
        if self.resultCode != eg.ID_TEST:
            self.dialog.buttonRow.applyButton.Enable(False)
            self.isDirty = False
        self.dialog.SetResult(*args)


    def AddLine(self, *items, **kwargs):
        self.maxRowNum = max(self.maxRowNum, len(items))
        self.lines.append((items, kwargs))


    def AddGrid(self, grid, vgap=6, hgap=5):
        columns = self.maxRowNum
        sizer = wx.GridBagSizer(vgap, hgap)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        rowFlagsGet = self.rowFlags.get
        colFlagsGet = self.colFlags.get
        for rowNum, (row, kwargs) in enumerate(grid):
            if kwargs.get("growable", False):
                sizer.AddGrowableRow(rowNum)
            for colNum, ctrl in enumerate(row):
                if ctrl is None:
                    ctrl = (1, 1)
                elif type(ctrl) in types.StringTypes:
                    ctrl = wx.StaticText(self, -1, ctrl)

                flags = rowFlagsGet(rowNum, 0) | colFlagsGet(colNum, 0)
                flags |= (wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                sizer.Add(ctrl, (rowNum, colNum), (1, 1), flags)

            if colNum < columns - 1:
                sizer.SetItemSpan(ctrl, (1, columns - colNum + 1))
        self.SetSizer(sizer)


    def EnableButtons(self, flag=True):
        """
        Enables/Disables the OK, Apply and Test buttons.

        Useful if you want to temporarily disable them, because the current
        settings have no valid state and later re-enable them.
        """
        self.buttonsEnabled = flag
        buttonRow = self.dialog.buttonRow
        buttonRow.okButton.Enable(flag)
        if buttonRow.testButton:
            buttonRow.testButton.Enable(flag)
        if flag and self.isDirty:
            buttonRow.applyButton.Enable(True)
        else:
            buttonRow.applyButton.Enable(False)

