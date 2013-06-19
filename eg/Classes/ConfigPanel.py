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


class ConfigDialog(eg.Dialog):

    def __init__(self, panel, item, resizable=False, showLine=True):
        self.panel = panel
        self.result = None
        self.greenlet = eg.Greenlet.getcurrent()
        self.showLine = showLine
        self.resizable = resizable
        
        addTestButton = False
        size = (450, 300)
        if isinstance(item, eg.PluginItem):
            title = eg.text.General.pluginLabel % item.executable.info.name
        elif isinstance(item, eg.EventItem):
            title = "EventItem"
            size = (450, 150)
        else:
            title = "%s: %s" % (item.executable.plugin.info.label, item.executable.name)
            addTestButton = True
        

        self.configureItem = eg.currentConfigureItem
        eg.currentConfigureItem.openConfigDialog = self
        
        dialogStyle = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU
        if resizable:
            dialogStyle |= wx.RESIZE_BORDER|wx.MAXIMIZE_BOX
        eg.Dialog.__init__(
            self, eg.document.frame, -1, title, style=dialogStyle
        )
        
        self.buttonRow = eg.ButtonRow(
            self, 
            (wx.ID_OK, wx.ID_CANCEL, wx.ID_APPLY),
            resizable
        )
        testButton = None
        if addTestButton:
            testButton = wx.Button(self, -1, eg.text.General.test)
            self.buttonRow.Add(testButton)
            testButton.Bind(wx.EVT_BUTTON, self.OnTestButton)
            
        self.buttonRow.testButton = testButton
            
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        paramSizer = wx.BoxSizer(wx.VERTICAL)
        self.headerBox = eg.HeaderBox(self, item)
        mainSizer.SetMinSize(size)
        flags = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER#|wx.ALIGN_CENTER_VERTICAL
        mainSizer.AddMany(
            (
                (self.headerBox, 0, wx.EXPAND, 0),
                (wx.StaticLine(self), 0, wx.EXPAND|wx.ALIGN_CENTER, 0),
                (paramSizer, 1, flags, 15),
            )
        )
        self.mainSizer = mainSizer
        self.sizer = paramSizer
        
        def ShowHelp(dummyEvent):
            self.configureItem.ShowHelp(self)
        wx.EVT_MENU(self, wx.ID_HELP, ShowHelp)
        
        self.SetAcceleratorTable(
            wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_HELP), ])
        )        


    @eg.LogIt
    def OnMaximize(self, event):
        if self.buttonRow.sizeGrip:
            self.buttonRow.sizeGrip.Hide()
        self.Bind(wx.EVT_SIZE, self.OnRestore)
        event.Skip()
            
            
    @eg.LogIt
    def OnRestore(self, event):
        if not self.IsMaximized():
            self.Unbind(wx.EVT_SIZE)
            if self.buttonRow.sizeGrip:
                self.buttonRow.sizeGrip.Show()
        event.Skip()
            
            
    def OnOK(self, event):
        self.result = wx.ID_OK
        self.greenlet.switch(wx.ID_OK)
        
        
    def OnCancel(self, event):
        self.result = wx.ID_CANCEL
        self.greenlet.switch(wx.ID_CANCEL)
        
        
    def OnApply(self, event):
        self.panel.SetFocus()
        self.result = wx.ID_APPLY
        self.greenlet.switch(wx.ID_APPLY)
        
        
    def OnTestButton(self, event):
        self.result = eg.ID_TEST
        self.greenlet.switch(eg.ID_TEST)
        
        
    def FinishSetup(self):
        # Temporary hack to fix button tabulator ordering problems.
        line = wx.StaticLine(self)
        self.mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER)
        buttonRow = self.buttonRow
        buttonRow.applyButton.MoveAfterInTabOrder(line)
        buttonRow.cancelButton.MoveAfterInTabOrder(line)
        buttonRow.okButton.MoveAfterInTabOrder(line)
        if buttonRow.testButton:
            buttonRow.testButton.MoveAfterInTabOrder(line)
        if not self.showLine:
            line.Hide()
        if self.resizable:
            self.mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND, 0)
        else:
            self.mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND|wx.RIGHT, 10)
        self.SetSizerAndFit(self.mainSizer)
        self.Fit() # without the addition Fit(), some dialogs get a bad size
        self.SetMinSize(self.GetSize())
        self.Centre()
        self.panel.SetFocus()
        
    

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
        self.nextResult = None
        self.greenlet = eg.Greenlet.getcurrent()
        item = eg.currentConfigureItem
            
        dialog = ConfigDialog(self, item, resizable, showLine)
        self.dialog = dialog
        wx.PyPanel.__init__(self, dialog, -1)
        self.lines = []
        dialog.sizer.Add(self, 1, wx.EXPAND)
        self.sizerProps = (6, 5)
        self.rowFlags = {}
        self.colFlags = {}
        self.shown = False
        self.maxRowNum = 0
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.args = None
        self.kwargs = None
        self.isDirty = False
        self.resultCode = None
        self.dialog.buttonRow.applyButton.Enable(False)
        
        
    @eg.LogIt
    def SetIsDirty(self, flag=True):
        self.isDirty = flag
        if flag:
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
            
        self.dialog.FinishSetup()        
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
        if not self.shown:
            self.FinishSetup()
        eg.Utils.EnsureVisible(self.dialog)
        self.dialog.Show()
        if self.nextResult == wx.ID_CANCEL:
            return False
        resultCode = eg.mainGreenlet.switch()
        self.resultCode = resultCode
        if resultCode == wx.ID_CANCEL:
            return False
        return resultCode

    
    def SetResult(self, *args, **kwargs):
        """
        Notifies the program of the current values of the configuration 
        controls.
        """
        self.args = args
        self.kwargs = kwargs
        if self.resultCode != eg.ID_TEST:
            self.dialog.buttonRow.applyButton.Enable(False)
            self.isDirty = False
        self.nextResult = self.greenlet.parent.switch(args)

    
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
        buttonRow = self.dialog.buttonRow
        buttonRow.okButton.Enable(flag)
        buttonRow.testButton.Enable(flag)
        if flag and self.isDirty:
            buttonRow.applyButton.Enable(True)
        else:
            buttonRow.applyButton.Enable(False)
        
            