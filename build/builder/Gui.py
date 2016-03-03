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

        # create controls for github connection
        ghSzr = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                 u"GitHub"), wx.VERTICAL)
        sb = self  # ghSzr.GetStaticBox()
        lblToken = wx.StaticText(sb, wx.ID_ANY, u"Token:")
        htmlToken = wx.HyperlinkCtrl(sb, wx.ID_ANY, u"?",
                                     u"https://github.com/settings/tokens")
        htmlToken.SetToolTipString(u"Personal access tokens function like "
                                   u"ordinary OAuth access tokens. They can "
                                   u"be used instead of a password for Git "
                                   u"over HTTPS, or can be used to "
                                   u"authenticate to the API over Basic "
                                   u"Authentication." )
        self.txtToken = wx.TextCtrl(sb, wx.ID_ANY, buildSetup.githubToken)

        tokenSzr = wx.BoxSizer(wx.HORIZONTAL)
        tokenSzr.Add(lblToken, 0, wx.ALIGN_CENTER_VERTICAL)
        tokenSzr.Add(htmlToken, 0, wx.ALIGN_CENTER_VERTICAL |
                     wx.LEFT | wx.RIGHT, 5)
        tokenSzr.Add(self.txtToken, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        lblUser = wx.StaticText(sb, wx.ID_ANY, u"User:")
        self.txtUser = wx.TextCtrl(sb, wx.ID_ANY, buildSetup.githubUser)
        lblRepo = wx.StaticText(sb, wx.ID_ANY, u"Repository:")
        self.txtRepo = wx.TextCtrl(sb, wx.ID_ANY, buildSetup.githubRepo)
        lblBranch = wx.StaticText(sb, wx.ID_ANY, u"Branch:")
        self.txtBranch = wx.TextCtrl(sb, wx.ID_ANY, buildSetup.githubBranch)

        repoSzr = wx.BoxSizer(wx.HORIZONTAL)
        repoSzr.Add(lblUser, 0, wx.ALIGN_CENTER_VERTICAL |
                    wx.LEFT | wx.RIGHT, 5)
        repoSzr.Add(self.txtUser, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        repoSzr.Add(lblRepo, 0, wx.ALIGN_CENTER_VERTICAL |
                    wx.LEFT | wx.RIGHT, 5)
        repoSzr.Add(self.txtRepo, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        repoSzr.Add(lblBranch, 0, wx.ALIGN_CENTER_VERTICAL |
                    wx.LEFT | wx.RIGHT, 5)
        repoSzr.Add(self.txtBranch, 1, wx.ALIGN_CENTER_VERTICAL |
                    wx.RIGHT, 5)

        ghSzr.Add(tokenSzr, 0, wx.ALL|wx.EXPAND, 5)
        ghSzr.Add(repoSzr, 1, wx.ALL|wx.EXPAND, )

        egSzr = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                               u"EventGhost"), wx.HORIZONTAL)
        sb = self  # egSzr.GetStaticBox()
        lblVersion = wx.StaticText(sb, wx.ID_ANY, u"Version to build:")
        self.versionStr = wx.TextCtrl(sb, wx.ID_ANY,
                                      value=buildSetup.appVersion)
        egSzr.Add(lblVersion, 0, wx.ALIGN_CENTER_VERTICAL |
                  wx.LEFT | wx.RIGHT, 5 )
        egSzr.Add(self.versionStr, 0, wx.ALIGN_CENTER_VERTICAL |
                  wx.LEFT | wx.RIGHT, 5)

        # combine all controls to a main sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(ghSzr, 0, wx.ALL, 5)
        mainSizer.Add(egSzr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        mainSizer.Add(sizer2, 1, wx.ALL | wx.EXPAND, 10)
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
        self.buildSetup.appVersion = self.versionStr.GetValue()
        self.buildSetup.githubToken = self.txtToken.GetValue()
        self.buildSetup.githubUser = self.txtUser.GetValue()
        self.buildSetup.githubRepo = self.txtRepo.GetValue()
        self.buildSetup.githubBranch = self.txtBranch.GetValue()
        self.buildSetup.config.SaveSettings()
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

