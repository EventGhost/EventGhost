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

# Local imports
import eg
from eg.Utils import SplitFirstParagraph

class ConfigDialog(eg.TaskletDialog):
    panel = None
    currentDialog = None

    def __init__(self, resizable=True, showLine=True):
        self.result = None
        self.showLine = showLine
        self.resizable = resizable
        addTestButton = False
        treeItem = self.treeItem
        name = treeItem.GetTypeName()
        firstParagraph, self.description = SplitFirstParagraph(
            treeItem.GetDescription()
        )
        size = (450, 300)
        if isinstance(treeItem, eg.PluginItem):
            title = eg.text.General.settingsPluginCaption
        elif isinstance(treeItem, eg.EventItem):
            title = eg.text.General.settingsEventCaption
            size = (450, 150)
        else:
            title = eg.text.General.settingsActionCaption
            addTestButton = True

        dialogStyle = wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU
        if resizable:
            dialogStyle |= wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
        eg.TaskletDialog.__init__(
            self, eg.document.frame, -1, title, style=dialogStyle
        )

        self.notebook = wx.Notebook(self)

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
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.headerBox = eg.HeaderBox(
            self,
            name,
            firstParagraph,
            treeItem.icon,
            treeItem.url if hasattr(treeItem, "url") else None
        )
        mainSizer.SetMinSize(size)
        mainSizer.AddMany(
            (
                (self.headerBox, 0, wx.EXPAND, 0),
                (wx.StaticLine(self), 0, wx.EXPAND | wx.ALIGN_CENTER, 0),
                (self.notebook, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 5),
            )
        )
        self.mainSizer = mainSizer

        def ShowHelp(dummyEvent):
            self.treeItem.ShowHelp(self)
        wx.EVT_MENU(self, wx.ID_HELP, ShowHelp)

        self.SetAcceleratorTable(
            wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_HELP), ])
        )

    @eg.LogItWithReturn
    def Configure(self, treeItem, *args):
        self.__class__.currentDialog = self
        self.treeItem = treeItem
        treeItem.openConfigDialog = self
        treeItem.Configure(*args)
        del treeItem.openConfigDialog

    def CreateHelpPanel(self):
        helpPanel = wx.Panel(self.notebook)
        helpPanel.SetBackgroundColour((255, 255, 255))
        htmlWindow = eg.HtmlWindow(helpPanel)
        htmlWindow.SetBasePath(self.treeItem.GetBasePath())
        htmlWindow.SetPage(self.description)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(htmlWindow, 1, wx.EXPAND)
        helpPanel.SetSizer(sizer)
        self.notebook.AddPage(helpPanel, "Description")
        return helpPanel

    def FinishSetup(self):
        # Temporary hack to fix button tabulator ordering problems.
        self.panel.FinishSetup()
        if self.description:
            self.CreateHelpPanel()
        #line = wx.StaticLine(self)
        #self.mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER)
        buttonRow = self.buttonRow
        buttonRow.applyButton.MoveAfterInTabOrder(self.notebook)
        buttonRow.cancelButton.MoveAfterInTabOrder(self.notebook)
        buttonRow.okButton.MoveAfterInTabOrder(self.notebook)
        if buttonRow.testButton:
            buttonRow.testButton.MoveAfterInTabOrder(self.notebook)
#        if not self.showLine:
#            line.Hide()
        if self.resizable:
            self.mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND, 0)
        else:
            self.mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND | wx.RIGHT, 10)
        self.SetSizerAndFit(self.mainSizer)
        self.Fit()  # without the addition Fit(), some dialogs get a bad size
        self.SetMinSize(self.GetSize())
        self.CentreOnParent()
        self.panel.SetFocus()
        eg.TaskletDialog.FinishSetup(self)

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

    def OnTestButton(self, event):
        self.DispatchEvent(event, eg.ID_TEST)
