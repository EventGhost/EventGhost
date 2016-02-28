# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import sys
import threading

import wx

import builder


class MainDialog(wx.Dialog):

    def __init__(self, buildSetup):
        self.buildSetup = buildSetup
        wx.Dialog.__init__(
            self, None, title="Build %s Installer" % buildSetup.name
        )

        # create controls
        self.ctrls = {}
        ctrlsSizer = wx.BoxSizer(wx.VERTICAL)
        for task in buildSetup.tasks:
            if not task.visible:
                continue
            section = task.GetId()
            ctrl = wx.CheckBox(self, -1, task.description)
            ctrl.SetValue(task.activated)
            ctrlsSizer.Add(ctrl, 0, wx.ALL, 5)
            self.ctrls[section] = ctrl
            if not task.enabled:
                ctrl.Enable(False)

        self.okButton = wx.Button(self, wx.ID_OK)
        self.okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.okButton.SetDefault()
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        # add controls to sizers
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(self.okButton)
        btnSizer.AddButton(self.cancelButton)
        btnSizer.Realize()

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(ctrlsSizer)

        lbl = wx.StaticText(self, wx.ID_ANY, 'Version:')
        self.versionStr = wx.TextCtrl(self, wx.ID_ANY, value=buildSetup.appVersion)
        szr = wx.BoxSizer(wx.HORIZONTAL)
        szr.Add(lbl, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        szr.Add(self.versionStr)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(szr, 0, wx.ALL, 5)
        mainSizer.Add(sizer2, 1, wx.ALL|wx.EXPAND, 0)
        mainSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.SetSizerAndFit(mainSizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnOk(self, dummyEvent):
        """ Handles a click on the Ok button. """
        self.okButton.Enable(False)
        self.cancelButton.Enable(False)
        #self.SetWindowStyleFlag(wx.CAPTION|wx.RESIZE_BORDER)
        for task in self.buildSetup.tasks:
            if not task.visible:
                continue
            section = task.GetId()
            if section in self.ctrls:
                ctrl = self.ctrls[section]
                task.activated = ctrl.GetValue()
                ctrl.Enable(False)
        self.buildSetup.config.SaveSettings()
        self.buildSetup.appVersion = self.versionStr.GetValue()
        thread = threading.Thread(target=self.DoMain)
        thread.start()


    def DoMain(self):
        builder.Tasks.Main(self.buildSetup)
        wx.CallAfter(self.OnExit)


    def OnExit(self):
        self.Destroy()
        sys.exit(0)


    def OnCancel(self, event):
        """ Handles a click on the cancel button. """
        event.Skip()
        self.Destroy()
        wx.GetApp().ExitMainLoop()


    def OnClose(self, event):
        """ Handles a click on the close box of the frame. """
        event.Skip()
        self.Destroy()
        wx.GetApp().ExitMainLoop()


def Main(buildSetup):
    app = wx.App(0)
    app.SetExitOnFrameDelete(True)
    mainDialog = MainDialog(buildSetup)
    mainDialog.Show()
    app.MainLoop()

