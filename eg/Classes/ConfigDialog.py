# -*- coding: utf-8 -*-
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


class ConfigDialog(eg.TaskletDialog):
    panel = None

    def __init__(self, item, resizable=False, showLine=True):
        self.item = item
        self.result = None
        self.showLine = showLine
        self.resizable = resizable

        addTestButton = False
        size = (450, 300)
        if isinstance(item, eg.PluginItem):
            title = eg.text.General.settingsPluginCaption
        elif isinstance(item, eg.EventItem):
            title = eg.text.General.settingsEventCaption
            size = (450, 150)
        else:
            title = eg.text.General.settingsActionCaption
            addTestButton = True

        self.configureItem = eg.currentConfigureItem
        eg.currentConfigureItem.openConfigDialog = self

        dialogStyle = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU
        if resizable:
            dialogStyle |= wx.RESIZE_BORDER|wx.MAXIMIZE_BOX
        eg.TaskletDialog.__init__(
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


    def FinishSetup(self):
        # Temporary hack to fix button tabulator ordering problems.
        self.panel.FinishSetup()
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
        self.CentreOnParent()
        self.panel.SetFocus()
        eg.TaskletDialog.FinishSetup(self)


    def OnTestButton(self, event):
        self.DispatchEvent(event, eg.ID_TEST)


    @eg.LogItWithReturn
    def Configure(self, item, *args):
        self.item = item
        item.openConfigDialog = self
        self.item.Configure(*args)
        del item.openConfigDialog

