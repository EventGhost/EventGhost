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
from Dialog import Dialog
import wx
import types

#def ConfigurationDialog(executable, *args, **kwargs):    
#    if executable == eg.currentConfigureItem.executable and eg.currentConfigureItem.openConfigDialog:
#        dialog = eg.currentConfigureItem.openConfigDialog
#        dialog.Freeze()
#        dialog.Clear()
#        return dialog
#    else:
#        return ConfigurationDialogBase(executable, *args, **kwargs)
#        
        
        
class ConfigurationDialog(Dialog):
    """
    A configuration dialog for all plug-ins and actions.
    """
    __postInited = False
    __isInited = False
    
    def __new__(cls, obj, *args, **kwargs):
        if obj == eg.currentConfigureItem.executable and eg.currentConfigureItem.openConfigDialog:
            self = eg.currentConfigureItem.openConfigDialog
            self.Freeze()
            self.Clear()
            self.Freeze()
            return self
        else:
            return eg.Dialog.__new__(cls, obj, *args, **kwargs)
        
        
    def __init__(self, obj, resizeable=None, showLine=True):
        eg.PrintError("eg.ConfigurationDialog is deprecated! " + repr(obj))
        if self.__isInited:
            return
        self.__isInited = True
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
        self.Freeze()
        
        self.buttonRow = eg.ButtonRow(
            self, 
            (wx.ID_OK, wx.ID_CANCEL, wx.ID_APPLY)
        )
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
            wx.AcceleratorTable(
                [
                    (wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_HELP),
                ]
            )
        )        
        
        

    def FinishSetup(self):
        if not self.__postInited:
            # Temporary hack to fix button ordering problems.
            line = wx.StaticLine(self)
            self.mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER)
            self.buttonRow.applyButton.MoveAfterInTabOrder(line)
            self.buttonRow.cancelButton.MoveAfterInTabOrder(line)
            self.buttonRow.okButton.MoveAfterInTabOrder(line)
            
            if not self.showLine:
                line.Hide()
            if self.resizeable:
                flag = wx.EXPAND
                border = 0
            else:
                flag = wx.EXPAND|wx.RIGHT
                border = 10
            self.mainSizer.Add(self.buttonRow.sizer, 0, flag, border)
            self.SetSizer(self.mainSizer)
            
        self.mainSizer.Fit(self)
        self.SetMinSize(self.GetSize())
        self.Layout()
        #self.Refresh()
        try:
            while self.IsFrozen():
                self.Thaw()
        except:
            pass
        if not self.__postInited:
            self.Centre()
        self.__postInited = True
        
        
    def Clear(self):
        #self.__postInited = False
        self.sizer.Clear(deleteWindows=True)
        #self.sizer.Add((0,0))
        for child in list(self.buttonRow.sizer.GetChildren())[:-3]:
            #if child.IsWindow():
                child.DeleteWindows()
        #print self.buttonRow.sizer.GetChildren()[:-3]
        
        
    def SetCallback(self, callback, *args, **kwargs):
        def OkCallWarpper(event):
            callback(wx.ID_OK, *args, **kwargs)
        self.buttonRow.okButton.Bind(wx.EVT_BUTTON, OkCallWarpper)
        def CancelCallWarpper(event):
            callback(wx.ID_CANCEL, *args, **kwargs)
        self.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, CancelCallWarpper)
        def ApplyCallWarpper(event):
            callback(wx.ID_APPLY, *args, **kwargs)
        self.buttonRow.applyButton.Bind(wx.EVT_BUTTON, ApplyCallWarpper)
        self.Bind(wx.EVT_CLOSE, CancelCallWarpper)
        
    
    def AffirmedShowModal(self):
        self.FinishSetup()
        if self.ShowModal() == wx.ID_OK:
            return True
        return False


    def AffirmedShowModal(self):
        gr1 = eg.Greenlet.getcurrent()
        self.FinishSetup()
        self.Show()
        self.Raise()
        def SwitchWrapper(resultCode):
            def wrapper(event):
                gr1.switch(resultCode)
            return wrapper
        self.buttonRow.okButton.Bind(wx.EVT_BUTTON, SwitchWrapper(wx.ID_OK))
        self.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, SwitchWrapper(wx.ID_CANCEL))
        self.buttonRow.applyButton.Bind(wx.EVT_BUTTON, SwitchWrapper(wx.ID_APPLY))
        self.Bind(wx.EVT_CLOSE, SwitchWrapper(wx.ID_CANCEL))
        
        self.result = eg.mainGreenlet.switch()
        #self.Hide()
        #self.Destroy()
        return self.result in (wx.ID_OK, wx.ID_APPLY)
    
    
#    def OnHelp(self, event):
#        self.configureItem.ShowHelp()
#

    def AddLabel(self, label):
        labelCtrl = wx.StaticText(self, -1, label)
        self.sizer.Add(labelCtrl, 0, wx.BOTTOM, 2)
        
        
    def AddCtrl(self, ctrl):
        self.sizer.Add(ctrl, 0, wx.BOTTOM, 10)
        
        
    def AddCtrlExpanded(self, ctrl):
        self.sizer.Add(ctrl, 0, wx.BOTTOM|wx.EXPAND, 10)
        
        
    def AddGrid(self, grid, vgap=10, hgap=5):
        columns = len(max(grid))
        sizer = wx.GridBagSizer(vgap, hgap)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        for rowNum, row in enumerate(grid):
            for colNum, ctrl in enumerate(row):
                if type(ctrl) in types.StringTypes:
                    ctrl = wx.StaticText(self, -1, ctrl)
                
                sizer.Add(
                    ctrl, 
                    (rowNum, colNum), 
                    (1,1), 
                    wx.ALIGN_CENTER_VERTICAL
                )
            if colNum < columns - 1:
                sizer.SetItemSpan(ctrl, (1, columns - colNum))
        self.sizer.Add(sizer)
        
