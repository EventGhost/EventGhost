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
# $LastChangedDate: 2007-11-14 04:19:28 +0100 (Mi, 14 Nov 2007) $
# $LastChangedRevision: 263 $
# $LastChangedBy: bitmonster $

import eg
import wx
import types


class ConfigDialog(eg.Dialog):

    def __init__(self, panel, obj, resizeable=None, showLine=True):
        self.panel = panel
        self.result = None
        self.gr = eg.Greenlet.getcurrent()
        self.showLine = showLine
        if resizeable is None:
            resizeable = bool(eg.debugLevel)
        self.resizeable = resizeable
        
        if isinstance(obj, eg.PluginClass):
            title = eg.text.General.pluginLabel % obj.name
            flags = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER
        else:
            title = "%s: %s" % (obj.plugin.info.label, obj.name)
            flags = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER

        self.configureItem = eg.currentConfigureItem
        eg.currentConfigureItem.openConfigDialog = self
        
        dialogStyle = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU
        if resizeable:
            dialogStyle |= wx.RESIZE_BORDER
        eg.Dialog.__init__(self, eg.document.frame, -1, title, style=dialogStyle)
        
        self.buttonRow = eg.ButtonRow(
            self, 
            (wx.ID_OK, wx.ID_CANCEL, wx.ID_APPLY)
        )
        self.buttonRow.okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.buttonRow.applyButton.Bind(wx.EVT_BUTTON, self.OnApply)
        self.Bind(wx.EVT_CLOSE, self.OnCancel)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        paramSizer = wx.BoxSizer(wx.VERTICAL)
        self.headerBox = eg.HeaderBox(self, obj)
        mainSizer.SetMinSize((450, 300))
        mainSizer.Add(self.headerBox, 0, wx.EXPAND, 0)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALIGN_CENTER, 0)
        mainSizer.Add(paramSizer, 1, flags|wx.ALIGN_CENTER_VERTICAL, 15)
        self.mainSizer = mainSizer
        self.sizer = paramSizer
        
        def ShowHelp(event):
            self.configureItem.ShowHelp()
        wx.EVT_MENU(self, wx.ID_HELP, ShowHelp)
        
        self.SetAcceleratorTable(
            wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_HELP), ])
        )        


    def OnOk(self, event):
        self.result = wx.ID_OK
        self.gr.switch(wx.ID_OK)
        
        
    def OnCancel(self, event):
        self.result = wx.ID_CANCEL
        self.gr.switch(wx.ID_CANCEL)
        
        
    def OnApply(self, event):
        self.panel.SetFocus()
        self.result = wx.ID_APPLY
        self.gr.switch(wx.ID_APPLY)
        
        
    def FinishSetup(self):
        # Temporary hack to fix button ordering problems.
        line = wx.StaticLine(self)
        self.mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.buttonRow.applyButton.MoveAfterInTabOrder(line)
        self.buttonRow.cancelButton.MoveAfterInTabOrder(line)
        self.buttonRow.okButton.MoveAfterInTabOrder(line)
        if not self.showLine:
            line.Hide()
        if self.resizeable:
            self.mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND, 0)
        else:
            self.mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND|wx.RIGHT, 10)
        self.SetSizerAndFit(self.mainSizer)
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Centre()
        self.Show()
        


class ConfigPanel(wx.PyPanel, eg.ControlProviderMixin):
    
    def __init__(self, executable, resizeable=None, showLine=True):
        self.nextResult = None
        self.gr = eg.Greenlet.getcurrent()
        dialog = ConfigDialog(self, executable, resizeable, showLine)
        self.dialog = dialog
        wx.PyPanel.__init__(self, dialog, -1)
        self.lines = []
        dialog.sizer.Add(self, 1, wx.EXPAND)
        self.sizerProps = (6, 5)
        self.rowFlags = {}
        self.colFlags = {}
        self.shown = False
        self.sizer = wx.BoxSizer(wx.VERTICAL)


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
        self.dialog.FinishSetup()        
    
    
    def Affirmed(self):
        if not self.shown:
            self.FinishSetup()
        if self.nextResult == wx.ID_CANCEL:
            return False
        resultCode = eg.mainGreenlet.switch()
        if resultCode == wx.ID_CANCEL:
            return False
        return resultCode

    
    def SetResult(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.nextResult = self.gr.parent.switch(args)

    
    def AddLine(self, *items, **kwargs):
        growable = kwargs.get("growable", False)
        self.lines.append((items, growable))


    def AddGrid(self, grid, vgap=6, hgap=5):
        columns = len(max(grid))
        sizer = wx.GridBagSizer(vgap, hgap)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        RowFlagsGet = self.rowFlags.get
        ColFlagsGet = self.colFlags.get
        for rowNum, (row, growable) in enumerate(grid):
            if growable:
                sizer.AddGrowableRow(rowNum)
            for colNum, ctrl in enumerate(row):
                if ctrl is None:
                    ctrl = (1, 1)
                elif type(ctrl) in types.StringTypes:
                    ctrl = wx.StaticText(self, -1, ctrl)
                
                flags = RowFlagsGet(rowNum, 0) | ColFlagsGet(colNum, 0)
                flags |= (wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                sizer.Add(ctrl, (rowNum, colNum), (1, 1), flags)
                
            if colNum < columns - 1:
                sizer.SetItemSpan(ctrl, (1, columns - colNum + 1))
        self.SetSizer(sizer)
        
        
